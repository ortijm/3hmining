from django.middleware.csrf import CsrfViewMiddleware


class TresHCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        # Evitar chequear CSRF si viene esteheader
        if request.META.get('HTTP_X_3HMINING') is not None:
            return None

        return super(TresHCsrfViewMiddleware, self).process_view(request, callback, callback_args, callback_kwargs)
