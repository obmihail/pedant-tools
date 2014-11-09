<!-- have not screenshot-->
%if img == False:
	<i class="status-{{status}} pedant-icon no-screenshot"></i>
%else:
	<a class="status-{{status}} fancybox" rel="group" href="{{img}}">
		<img class="lazy" data-original="{{img}}" alt="{{alt}}" />
	</a>