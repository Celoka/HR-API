from sqlalchemy import desc, asc

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
    
    def fetch_all(self):
        return self._model.query.paginate(error_out=False)

    def filter_by(self, **kwargs):
        return self._model.query.filter_by(**kwargs).paginate(error_out=False)

    def filter_first(self, **kwargs):
        return self._model.query.filter_by(**kwargs).first()
    
    def count(self):
        return self._model.query.count()
    
    def order_by(self, *args):
        return self._model.query.order_by(*args)
    
    def filter_and_count(self, **kwargs):
        return self._model.query.filter_by(**kwargs).count()
    
    def filter_by_desc(self, *args, **kwargs):
        return self._model.query.filter_by(**kwargs).order_by(desc(*args)) \
            .paginate(error_out=False)

    def filter_by_asc(self, *args, **kwargs):
        return self._model.query.filter_by(**kwargs).order_by(asc(*args)) \
            .paginate(error_out=False)
