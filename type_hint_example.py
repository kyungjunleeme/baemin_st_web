from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from django.db import models
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View
from django.views.generic.detail import (
    BaseDetailView,
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from typing_extensions import Literal

_FormT = TypeVar("_FormT", bound=BaseForm)
_ModelFormT = TypeVar("_ModelFormT", bound=BaseModelForm)
_T = TypeVar("_T", bound=models.Model)


class AbstractFormMixin(Generic[_FormT], ContextMixin):
    initial: Dict[str, Any] = ...
    form_class: Optional[Type[_FormT]] = ...
    success_url: Optional[Union[str, Callable[..., Any]]] = ...
    prefix: Optional[str] = ...

    def get_initial(self) -> Dict[str, Any]:
        ...

    def get_prefix(self) -> Optional[str]:
        ...

    def get_form_kwargs(self) -> Dict[str, Any]:
        ...

    def get_success_url(self) -> str:
        ...


class FormMixin(Generic[_FormT], AbstractFormMixin):
    def get_form_class(self) -> Type[_FormT]:
        ...

    def get_form(self, form_class: Optional[Type[_FormT]] = ...) -> BaseForm:
        ...

    def form_valid(self, form: _FormT) -> HttpResponse:
        ...

    def form_invalid(self, form: _FormT) -> HttpResponse:
        ...


class ModelFormMixin(
    Generic[_T, _ModelFormT], AbstractFormMixin, SingleObjectMixin[_T]
):
    fields: Optional[Union[Sequence[str], Literal["__all__"]]] = ...

    def get_form_class(self) -> Type[_ModelFormT]:
        ...

    def get_form(self, form_class: Optional[Type[_ModelFormT]] = ...) -> BaseModelForm:
        ...

    def form_valid(self, form: _ModelFormT) -> HttpResponse:
        ...

    def form_invalid(self, form: _ModelFormT) -> HttpResponse:
        ...


class ProcessFormView(View):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        ...

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        ...

    def put(self, *args: str, **kwargs: Any) -> HttpResponse:
        ...


class BaseFormView(FormMixin[_FormT], ProcessFormView):
    ...


class FormView(TemplateResponseMixin, BaseFormView[_FormT]):
    ...


class BaseCreateView(ModelFormMixin[_T, _ModelFormT], ProcessFormView):
    ...


class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView[_T, _ModelFormT]):
    ...


class BaseUpdateView(ModelFormMixin[_T, _ModelFormT], ProcessFormView):
    ...


class UpdateView(SingleObjectTemplateResponseMixin, BaseUpdateView[_T, _ModelFormT]):
    ...


class DeletionMixin:
    success_url: Optional[str] = ...

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        ...

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        ...

    def get_success_url(self) -> str:
        ...


class BaseDeleteView(DeletionMixin, BaseDetailView):
    ...


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    ...
