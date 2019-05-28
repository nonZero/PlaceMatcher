export default [
	{
		name: 'OpenStreetMap',
		visible: true,
		attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
		url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
	},
	{
		name: 'Israel Hiking Map',
		visible: false,
		attribution: 'OSM',
		url: 'https://israelhiking.osm.org.il/Tiles/{z}/{x}/{y}.png'
	},	{
		name: 'ESRI',
		visible: false,
		attribution: '&copy; ESRI',
		url: 'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
	},
	{
		name: 'מנדטורית שנות הארבעים',
		visible: false,
		attribution: '',
		maxZoom: 16,
		url: 'https://palopenmaps.org/tiles/pal20k-1940s/{z}/{x}/{y}.jpg'
	},
	{
		name: 'OpenTopoMap',
		visible: false,
		url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
		attribution: 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
	}
]
