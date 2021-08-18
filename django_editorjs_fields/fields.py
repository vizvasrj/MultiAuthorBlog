from django.core import checks
from django.db.models import Field
from django.forms import Textarea

from .config import DEBUG
from .widgets import EditorJsWidget

try:
    # pylint: disable=ungrouped-imports
    from django.db.models import JSONField  # Django >= 3.1
except ImportError:
    HAS_JSONFIELD = False
else:
    HAS_JSONFIELD = True

__all__ = ['EditorJsTextField', 'EditorJsJSONField']


class FieldMixin(Field):
    def get_internal_type(self):
        return 'TextField'


class EditorJsFieldMixin:
    def __init__(self, plugins, tools, **kwargs):
        self.use_editorjs = kwargs.pop('use_editorjs', True)
        self.plugins = plugins
        self.tools = tools
        self.config = {}

        if 'autofocus' in kwargs:
            self.config['autofocus'] = kwargs.pop('autofocus')
        if 'hideToolbar' in kwargs:
            self.config['hideToolbar'] = kwargs.pop('hideToolbar')
        if 'inlineToolbar' in kwargs:
            self.config['inlineToolbar'] = kwargs.pop('inlineToolbar')
        if 'readOnly' in kwargs:
            self.config['readOnly'] = kwargs.pop('readOnly')
        if 'minHeight' in kwargs:
            self.config['minHeight'] = kwargs.pop('minHeight')
        if 'logLevel' in kwargs:
            self.config['logLevel'] = kwargs.pop('logLevel')
        if 'placeholder' in kwargs:
            self.config['placeholder'] = kwargs.pop('placeholder')
        if 'defaultBlock' in kwargs:
            self.config['defaultBlock'] = kwargs.pop('defaultBlock')
        if 'sanitizer' in kwargs:
            self.config['sanitizer'] = kwargs.pop('sanitizer')
        if 'i18n' in kwargs:
            self.config['i18n'] = kwargs.pop('i18n')

        super().__init__(**kwargs)

    def formfield(self, **kwargs):
        if self.use_editorjs:
            kwargs['widget'] = EditorJsWidget(
                self.plugins, self.tools, self.config, **kwargs)
        else:
            kwargs['widget'] = Textarea(**kwargs)

        # pylint: disable=no-member
        return super().formfield(**kwargs)


class EditorJsTextField(EditorJsFieldMixin, FieldMixin):
    # pylint: disable=useless-super-delegation
    def __init__(self, plugins=None, tools=None, **kwargs):
        super().__init__(plugins, tools, **kwargs)


class EditorJsJSONField(EditorJsFieldMixin, FieldMixin):
    # pylint: disable=useless-super-delegation
    def __init__(self, plugins=None, tools=None, **kwargs):
        super().__init__(plugins, tools, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_supported_json())
        return errors

    def _check_supported_json(self):
        if not HAS_JSONFIELD and DEBUG:
            return [
                checks.Warning(
                    'You don\'t support JSONField, please use'
                    'EditorJsTextField instead of EditorJsJSONField',
                    obj=self,
                )
            ]
        return []
