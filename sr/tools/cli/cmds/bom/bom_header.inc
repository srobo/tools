<html>
<head>
<title>Student Robotics Bill of Materials%(title)s</title>
<style>
td {
  border-style: solid none none none;
  border-width: 1px;
  padding: 1px 4px;
  border-right: 1px solid #eee;
}
td:last-child {
  border-right: none;
}
th {
  border-style: none none solid none;
  border-width: 2px;
}

#board_image {
  position: relative;
}
#crosshair {
  position: absolute;
}
</style>
<script type="text/javascript">
%(xy)s
function highlight(refdes) {
    ch = document.getElementById("crosshair");
    var data = xy[refdes];
    ch.style.bottom = data.y;
    ch.style.left = data.x;
}
</script>
</head>
<body>
<div id="board_image">
%(img_tag)s
%(cross_hair)s
</div>
<table style="border-style:none;border-spacing:0;">
<thead>
<tr>
<th>Line No.</th>
<th>Internal Part No.</th>
<th>Qty</th>
<th>Value/Description</th>
<th>Package</th>
<th>Distributor</th>
<th>Distributor Order No.</th>
<th>Manufacturer</th>
<th>Part No.</th>
<th>Designators</th>
</tr>
</thead>
<tbody>
