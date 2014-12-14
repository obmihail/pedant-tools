% if len( crumbs ) > 0:
	<ol class="breadcrumb">
	% for crumb in crumbs:
		% if not crumb == crumbs[-1]:
			<li class="">
				<a href='{{ crumb[0] }}'>{{ crumb[1] }}</a>
			</li>
		% else:
			<li class="active">{{ crumb[1] }}</li>
		% end
  	% end
	</ol>
% end