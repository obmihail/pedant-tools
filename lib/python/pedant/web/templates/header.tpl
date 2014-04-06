<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>{{title}}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="Web interface for pedant testing tool">
	<meta name="author" content="Oblozhikhin Mikhail">
	<!-- bootstrap -->
	<!-- <link href="/assets/css/bootstrap.css" rel="stylesheet"> -->
	<link href="/assets/css/bootstrap.min.css" rel="stylesheet">
	<style>body{padding-top:60px; }</style>
	<link href="/assets/css/bootstrap-responsive.css" rel="stylesheet">
	<!-- pedant -->
	<link href="/assets/css/pedant.css" rel="stylesheet">
	<!-- add fancyBox -->
	<link rel="stylesheet" href="/assets/css/fancybox/source/jquery.fancybox.css?v=2.1.5" type="text/css" media="screen" />
	<!-- jquery -->
	<script src="/assets/scripts/jquery.min.js" type="text/javascript"></script>
	<!-- select2 -->
	<link rel="stylesheet" href="/assets/css/select2.min.css" type="text/css" media="screen" />
	<script src="/assets/scripts/select2.min.js" type="text/javascript"></script>
	<!-- pedant -->
	<script type="text/javascript" src="/assets/scripts/pedant.functions.js"></script>
	<script type="text/javascript" src="/assets/scripts/pedant.js"></script>
	<!-- bootstrap -->
	<script src="/assets/scripts/bootstrap.min.js" type="text/javascript"></script>
	<!-- fancy box wheel -->
	<script type="text/javascript" src="/assets/scripts/fancybox/lib/jquery.mousewheel-3.0.6.pack.js"></script>
	<script type="text/javascript" src="/assets/scripts/fancybox/source/jquery.fancybox.pack.js?v=2.1.5"></script>
	<!-- alerts -->
	<script type="text/javascript" src="/assets/scripts/jquery.bsAlerts.js"></script>
	<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->
	<!-- lazy-load plugin -->
	<script type="text/javascript" src="/assets/scripts/jquery.lazyload.min.js"></script>
	<script type="text/javascript" src="/assets/scripts/lodash.js"></script>
	
	<link rel="apple-touch-icon-precomposed" sizes="144x144" href="/assets/ico/apple-touch-icon-144-precomposed.png">
	<link rel="apple-touch-icon-precomposed" sizes="114x114" href="/assets/ico/apple-touch-icon-114-precomposed.png">
	<link rel="apple-touch-icon-precomposed" sizes="72x72" href="/assets/ico/apple-touch-icon-72-precomposed.png">
	<link rel="apple-touch-icon-precomposed" href="/assets/ico/apple-touch-icon-57-precomposed.png">
	<link rel="shortcut icon" href="/assets/ico/favicon.png">
</head>
<body>
	<!-- Navigation bar -->
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
				<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</a>
				<a class="navbar-brand" href="/">&lt; Home</a>
				<div class="nav-collapse collapse">
					% setdefault('menu', [ {'name':'MockMenu1','active':False,'href':'#1'}, {'name':'MockMenu2','active':True,'href':'#2'}, {'name':'MockMenu3','active':False,'href':'#3'} ])
					<!-- <ul class="nav">
						% for item in menu:
							%if item['active']:
								<li class="active">
							%else:
								<li>
							%end
							<a href="/{{item['href']}}">{{item['name']}}</a></li>
						% end
					</ul> -->
				</div> 
			</div>
		</div>
	</div>


<div data-alerts="alerts" data-titles="{'warning': '<em>Warning!</em>'}" data-ids="myid" data-fade="30000" ></div>

<!-- variables -->
% if defined('js_vars'):
	<script>
%	for var_name, value in js_vars.iteritems():
		var {{!var_name}} = {{!value}}
%	end
	</script>
% end

<div class="container">