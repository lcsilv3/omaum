# Revisão da Funcionalidade: templates

## Arquivos de Template:


### Arquivo: templates\includes\form_errors.html

html
{% if form.errors %}
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            <strong>Erro:</strong>
            <ul>
                {% for error in form.non_field_errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}

    {% for field in form %}
        {% if field.errors %}
            <div class="alert alert-danger">
                <strong>{{ field.label }}:</strong>
                <ul>
                    {% for error in field.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    {% endfor %}
{% endif %}



### Arquivo: templates\includes\form_field.html

html
<div class="mb-3">
    <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}
        <div class="invalid-feedback d-block">
            {% for error in field.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
    {% if field.help_text %}
        <small class="form-text text-muted">{{ field.help_text }}</small>
    {% endif %}
</div>

