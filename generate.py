import yaml
import os
import jinja2

with open("startupconfig.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


def createConfig(config):
	''' Create Config with Proxies for hosting local sites '''

	def render(tpl_path, context):
	    path, filename = os.path.split(tpl_path)
	    print 'generating %s configuration for %s...'%(tpl_path ,context['name'])
            if 'http_redir' not in context:
                context['http_redir']=True
            return jinja2.Environment(
	        loader=jinja2.FileSystemLoader(path or './')
	    ).get_template(filename).render(context)

	for i in config['services']:
                if not i['url'] or len(i['url'])==0 or i['url'].strip() == "":
                    pass
                else:
		    contents = render('./template.conf', i)
		    f = open("/etc/apache2/sites-enabled/"+i['name']+'.conf', 'w')
		    f.write(contents)
                if not ('command' in i) or len(i['command'])==0:
                    pass
                else:
		    contents = render('./template.service', i)
		    f = open("/etc/systemd/system/"+i['name']+'.service', 'w')
		    f.write(contents)

createConfig(config)
