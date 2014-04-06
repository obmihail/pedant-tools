% include('header.tpl', title='Edit project' )

% if not project:
% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('','New') ])
<h3>New project:</h3>
% else:
% include('breadcrumbs.tpl', crumbs = [ ('/','Home'), ('/projects','Projects'), ('/projects/%s'%project,project), ('','Edit') ])
<h3>Edit project: {{ project }}</h3>
% end

<!-- CONFIG TEMPLATE -->
<script charset="UTF-8">
$(document).ready(function() {
	load_project_config(function(data){
		//
		$('#browsers-table').html(_.template( $('#browser-table-tpl').html(), { browsers: config.browsers } ) )
		//
		$('#modes-table').html(_.template( $('#modes-table-tpl').html(), { modes: config.modes } ) )
		//
		$('#states-table').html(_.template( $('#states-table-tpl').html(), { states: states } ) )
		//
		$('#name').val(config['name'])
		//
		$('#base_url').val(config.base_url)
		//
		if (config.diffs_saving){
			$('.diffs-checkbox').click()
		}
		//urls
		$('#urls').val(data.urls.join("\n"))
		//threads limit
		$('#threads').val(config.threads)
		})
	$('#project-state-modal').on('show.bs.modal', function (event) {
		state = $(event.relatedTarget).data('config')
		console.log(state)
		var html = _.template( $('#project-states-modal-tpl').html(), { states: [state] } )
		$(this).find('.modal-content').html(html)
		//set body content
	})

});
</script>

% include('client_side_templates.tpl')
% include('prj_edit_modals.tpl')

<form role="form">
	<div class="form-group">
		<label for="name">Project name</label>
		<input type="text" class="form-control name" id="name" placeholder="Enter new project name" value="">
	</div>
	<div class="form-group">
		<label for="urls">Urls for scanning (plain text, new line - new url)</label>
		<textarea class="form-control" id="urls" rows="7"></textarea>
	</div>
	<div class="form-group">
		<label for="url_mask">Base url ( need for build urls )</label>
		<input type="text" class="form-control" id="base_url" placeholder="http://myproject.lcl/" value="">
	</div>
	<div class="form-group">
		<label for="threads">Maximum threads count</label>
		<input type="number" class="form-control" id="threads" min="1" max="50" placeholder="Threads" value="">
	</div>
	<div class="checkbox">
		<label>
			<input class="diffs-checkbox" type="checkbox"> Generate diffs images for screenshots (in screens build)
		</label>
	</div>
	<div class="form-group">
		<table class="table table-bordered table-hover table-fixed-wrap" id="browsers-table" name="browsers">
		</table>
		<button type="button" class="btn add-browser" data-toggle="modal" data-target="#edit_browser_modal" data-mode="add" style="display: block; width: 100%;">ADD BROWSER</button>
	</div>
	<div class="form-group">
		<table class="table table-condensed table-fixed-wrap" id="modes-table" name="modes"></table>
		<button type="button" class="btn add-launch-mode" data-toggle="modal" data-target="#edit_launch_mode_modal" data-mode="add" style="display: block; width: 100%;">ADD LAUNCH MODE</button>
		</div>
	<div class="form-group">
		<table class="table table-condensed table-fixed-wrap" id="states-table" name="states"></table>
	</div>
</form>

<p>------------------</p>
% if project == '':
		<button id="dLabel" class="btn save-project" data-url="/api/projects/create" role="button">ADD</button>
% else:
		<button id="dLabel" class="btn save-project" data-url="/api/projects/{{project}}/update" role="button">Save configuration</button>
% end
% include('footer.tpl')