<!-- BRO EDITOR MODAL -->
<div class="modal fade" id="editBrowserModal" tabindex="-1" role="dialog" aria-labelledby="browserEditor" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
    <h4 class="modal-title" id="browserEditor">Title</h4>
  </div>
  <div class="modal-body">
    <form role="form" name="browser-editor">
	      	  <div class="form-group">
	      	  	<label for="browser-type">Browser type</label>
			    <select class="form-control browser-type" id="browser-type">
					<option>ANDROID</option>
					<option>CHROME</option>
					<option>FIREFOX</option>
					<option>INTERNETEXPLORER</option>
					<option>IPAD</option>
					<option>IPHONE</option>
					<option>OPERA</option>
					<option>PHANTOMJS</option>
					<option>SAFARI</option>
				</select>
			  </div>
			  <div class="form-group">
			    <label for="browser-unid">Unique name for browser</label>
			    <input type="text" class="form-control" id="browser-unid" placeholder="Enter unid" value="">
			  </div>
			  <div class="form-group">
			    <label for="wd-url">Webdriver url</label>
			    <input type="text" class="form-control" id="wd-url" placeholder="Enter webdriver url" 
					value="">
			  </div>
			  <div class="form-group">
			    <label for="window-w">Window width</label>
			    <input type="number" class="form-control" id="window-w" min="100" max="5000" placeholder="Enter window width" value="">
			    <label for="window-h">Window height</label>
			    <input type="number" class="form-control" id="window-h" min="100" max="5000" placeholder="Enter window height"
			    	value="">
			  </div>
			  <div class="form-group">
			    <label for="browser-info">Description</label>
			    <textarea class="form-control" id="browser-info" rows="2"></textarea>
			  </div>
			  <div class="form-group">
			    <label for="browser-caps">Desired capabilities</label>
			    <textarea class="form-control" id="browser-caps" rows="3"></textarea>
			  </div>
		</form>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
    <button type="button" class="btn btn-primary save-browser">Save</button>
  </div>
</div>
</div>
</div>

<!-- BRO DELETE MODAL -->
<div class="modal fade" id="deleteBrowserModal" tabindex="-1" role="dialog" aria-labelledby="browserConfirm" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
    <h4 class="modal-title" id="browserConfirm">Delete browser?</h4>
  </div>
  <div class="modal-body">
  	<p>Are you shure? This operation remove browser from all launch modes</p>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
    <button type="button" class="btn btn-primary delete-browser">Delete</button>
  </div>
</div>
</div>
</div>

<!-- PROJECT MODE DELETE MODAL -->
<div class="modal fade" id="deleteLMModal" tabindex="-1" role="dialog" aria-labelledby="modeConfirm" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
    <h4 class="modal-title" id="modeConfirm">Delete mode?</h4>
  </div>
  <div class="modal-body">
  	<p>Are you shure? This operation remove launch mode</p>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
    <button type="button" class="btn btn-primary delete-mode">Delete</button>
  </div>
</div>
</div>
</div>

<!-- PROJECT MODE MODAL -->
<div class="modal fade" id="editLMModal" tabindex="-1" role="dialog" aria-labelledby="modeEditor" aria-hidden="true">
<div class="modal-dialog">
<div class="modal-content">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
    <h4 class="modal-title" id="modeEditor">Mode editor</h4>
  </div>
  <div class="modal-body">
    <form role="form" name="browser-editor">
			  <div class="form-group">
			    <label for="mode-name">Name</label>
			    <input type="text" class="form-control" id="mode-name" placeholder="Enter launch mode name" 
					value="">
			  </div>
			  <div class="form-group">
			    	
			    	<div class="checkbox browsers-for-mode">
						<!-- lodash put checkboxes here from template from #browsers-for-mode-checkboxes-tpl -->
					</div>
			  </div>
		</form>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
    <button type="button" class="btn btn-primary save-mode">Save</button>
  </div>
</div>
</div>
</div>