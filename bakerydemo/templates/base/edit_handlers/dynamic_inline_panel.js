{% load l10n %}
{% load wagtailadmin_tags %}
(function() {
    const options = {
        formsetPrefix: "id_{{ self.formset.prefix }}",
        emptyChildFormPrefix: "{{ self.empty_child.form.prefix }}",
        canOrder: {% if can_order %}true{% else %}false{% endif %},
        maxForms: {{ self.formset.max_num|unlocalize }}
    };

    var panel = InlinePanel(options); // changed (opts pulled up)

    {% for child in self.children %}
        panel.initChildControls("{{ child.form.prefix }}");
    {% endfor %}

    panel.setHasContent();
    panel.updateMoveButtonDisabledStates();
    panel.updateAddButtonState();

    {% if self.dynamic_content %}

    function buildExpandingFormset(prefix, opts = {}) {
        const addButton = $('#' + prefix + '-' + opts.extra +'-ADD'); // changed
        const formContainer = $('#' + prefix + '-FORMS');
        const totalFormsInput = $('#' + prefix + '-TOTAL_FORMS');
        let formCount = parseInt(totalFormsInput.val(), 10);

        console.log('buildExpandingFormset', {prefix, opts,addButton, formContainer });
        
        if (opts.onInit) {
            for (let i = 0; i < formCount; i++) {
            opts.onInit(i);
            }
        }
        
        let emptyFormTemplate = document.getElementById(prefix + '-' + opts.extra + '-EMPTY_FORM_TEMPLATE'); // changed
        if (emptyFormTemplate.innerText) {
            emptyFormTemplate = emptyFormTemplate.innerText;
        } else if (emptyFormTemplate.textContent) {
            emptyFormTemplate = emptyFormTemplate.textContent;
        }
        
        // eslint-disable-next-line consistent-return
        addButton.on('click', () => {
            if (addButton.hasClass('disabled')) return false;
            const newFormHtml = emptyFormTemplate
            .replace(/__prefix__/g, formCount)
            .replace(/<-(-*)\/script>/g, '<$1/script>');
            formContainer.append(newFormHtml);
            if (opts.onAdd) opts.onAdd(formCount);
            if (opts.onInit) opts.onInit(formCount);
        
            formCount++;
            totalFormsInput.val(formCount);
        });
    }

    function onAdd(formCount) {
        let self = panel;
        const newChildPrefix = options.emptyChildFormPrefix.replace(/__prefix__/g, formCount);
        self.initChildControls(newChildPrefix);
        if (options.canOrder) {
          /* NB form hidden inputs use 0-based index and only increment formCount *after* this function is run.
          Therefore formcount and order are currently equal and order must be incremented
          to ensure it's *greater* than previous item */
          $('#id_' + newChildPrefix + '-ORDER').val(formCount + 1);
        }
  
        self.updateMoveButtonDisabledStates();
        self.updateAddButtonState();
    }

    {% for item in self.dynamic_content %}
        buildExpandingFormset("id_{{ self.formset.prefix }}", { extra: "{{ item.prefix }}", onAdd });
    {% endfor %}

    {% endif %}
})();
