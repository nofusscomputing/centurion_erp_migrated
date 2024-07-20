from django.forms import ValidationError

from assistance.models.knowledge_base import KnowledgeBaseCategory

from core.forms.common import CommonModelForm



class KnowledgeBaseCategoryForm(CommonModelForm):

    __name__ = 'asdsa'

    class Meta:

        fields = '__all__'

        model = KnowledgeBaseCategory

    prefix = 'knowledgebase_category'


    def clean(self):
        
        cleaned_data = super().clean()

        target_team = cleaned_data.get("target_team")
        target_user = cleaned_data.get("target_user")


        if target_team and target_user:

            raise ValidationError('Both a Target Team or Target User Cant be assigned at the same time. Use one or the other or None')


        return cleaned_data

