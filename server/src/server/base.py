from typing import Callable, Dict


class DefaultRouter:
    def __init__(self):
        self.routes: Dict[str, Callable] = {}

    def register(self, path: str):
        def _register(fn):
            self.routes[path] = fn

            def _wrapper(*args, **kwargs):
                pass

            return _wrapper

        return _register

    def include_router(self, router: 'DefaultRouter'):
        self.routes.update(router.routes)

    def get_endpoint(self, path: str):
        if path in self.routes:
            return self.routes[path]
