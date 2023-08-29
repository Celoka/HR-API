class BaseService:

    def __init__(self, _model):
        self._model = _model

    def get(self, *args):
        return self._model.query.get(*args)

    def update(self, model_instance, **kwargs):
        for key, val in kwargs.items():
            setattr(model_instance, key, val)
        model_instance.save()
        return model_instance

    def filter_by(self, **kwargs):
        return self._model.query.filter_by(**kwargs).paginate(error_out=False)

    def filter_first(self, **kwargs):
        return self._model.query.filter_by(**kwargs).first()
