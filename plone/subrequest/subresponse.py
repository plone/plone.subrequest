# -*- coding: utf-8 -*-
from ZPublisher.HTTPResponse import HTTPResponse
from ZPublisher.Iterators import IStreamIterator

import io
import six


try:
    from plone.app.blob.iterators import BlobStreamIterator
except ImportError:
    class BlobStreamIterator:
        pass


class SubResponse(HTTPResponse):

    def setBody(self, body, title='', is_error=0, **kw):
        """Accept either a stream iterator or a string as the body."""
        if not IStreamIterator.providedBy(body):
            return HTTPResponse.setBody(self, body, title, is_error, **kw)
        assert not self._wrote
        if isinstance(body, BlobStreamIterator):
            body = body.blob  # A BlobFile
        if hasattr(body, 'seek') \
           and hasattr(body, 'read') and \
           hasattr(body, 'close'):
            self.stdout = body
            self._wrote = 1
            return
        try:
            while True:
                chunk = next(body)
                self.write(chunk)
        except StopIteration:
            pass

    def __str__(self):
        return str(self.body)

    def outputBody(self):
        """Output the response body."""
        if not self._wrote:
            body = self.body
            if isinstance(self.stdout, io.BufferedIOBase)\
                    and isinstance(body, six.text_type):
                body = body.encode('utf-8')
            elif isinstance(self.stdout, io.TextIOBase)\
                    and isinstance(body, six.binary_type):
                body = body.decode('utf-8')
            self.stdout.write(body)
            self._wrote = 1

    def getBody(self):
        """Return the body, however it was written."""
        if not self._wrote:
            return self.body
        stdout = self.stdout
        try:
            if hasattr(stdout, 'getvalue'):
                return stdout.getvalue()
            else:
                stdout.seek(0, 0)
                return stdout.read()
        finally:
            stdout.close()
