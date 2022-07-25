module.exports = {
  apps: [{
    script: '{{ service_path }}/build/server.js',
    name: '{{ service_name }}-volto',
    cwd: '{{ service_path }}',
    namespace: '{{ volto_port }}',
    env: {
      PORT: '{{ volto_port }}',
      NODE_ENV: 'production'
    }
  },
  {% if service_api_instances|length == 1 and no_api is not defined %}
  {
    script: '{{ service_path }}/api/bin/instance',
    args: 'console',
    name: '{{ service_name }}-api',
    cwd: '{{ service_path }}',
    interpreter: '{{ pipenv_interpreter.stdout }}/bin/python',
    namespace: '{{ api_port }}'
  }
  {% endif %}
  {% if service_api_instances|length > 1 and no_api is not defined %}
  {% for instance in service_api_instances %}
  {% set iname = (instance.replace('instance','')|int) -1  %}
  {
    script: '{{ service_path }}/api/bin/{{instance}}',
    args: 'console',
    name: '{{ service_name }}-api-{{instance}}',
    cwd: '{{ service_path }}',
    interpreter: '{{ pipenv_interpreter.stdout }}/bin/python',
    namespace: '{{ api_port[iname] }}'
  },
  {% endfor %}
  {
    script: '{{ service_path }}/api/bin/zeo',
    args: 'fg',
    name: '{{ service_name }}-api-zeo',
    cwd: '{{ service_path }}',
    interpreter: '{{ service_path }}/api/bin/python',
    namespace: '{{ zeo_port }}'
  }
  {% endif %}
  ]
}
