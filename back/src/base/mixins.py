class PartialUpdateMixin:
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
