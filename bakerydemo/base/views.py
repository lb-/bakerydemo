from wagtail.contrib.modeladmin.views import IndexView


class KanbanView(IndexView):

    def get_template_names(self):
        return self.model_admin.get_templates('kanban')
