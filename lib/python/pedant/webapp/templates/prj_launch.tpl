% include('header.tpl', title='Pedant main page', breadcrumbs = crumbs )
<div class="container">

<h3>Launch {{config['prj_name']}}</h3>

<script type="text/javascript">

	var config = {{ !config_str }}

	var update_interval_id = false;

</script>

<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="2000" ></div>
<div>

<div class="form-group">
	<label for="mode-choise">Project modes</label>
	<select class="form-control mode-choise" id="mode-choise">
		% for modename,mode in config["modes"].iteritems():
			<option>{{modename}}</option>
		% end
	</select>
</div>
<div class="form-group">
	<button type="button" class="btn btn-default start-project" data-url="/ajax/projects/{{config['prj_name']}}/launch/start">RUN</button>
	<button type="button" class="btn btn-default stop-project" data-url="/ajax/projects/{{config['prj_name']}}/launch/stop">STOP</button>
	<a class="btn btn-default" target="_blank" href="/projects/{{config['prj_name']}}/reports/last">Last project detail report</a>
	<h4>Status: <span class='text-danger current-status'>N\A</span></h4>
</div>
</div>

<!-- WORK RESULTS -->
<div class="container-fluid">
    <div class="row"> <!-- Give this div your desired background color -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                	<textarea class="launch-info col-md-12" rows="20"></textarea>
                </div
            </div>
        </div>
    </div>
</div>

</div>
% include('footer.tpl')