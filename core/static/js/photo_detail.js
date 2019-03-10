// const app = new Vue({
// 	el: '#app',
// 	data: {
// 		message: 'Hello Vue!'
// 	}
// });

L.NumberedDivIcon = L.Icon.extend({
	options: {
		iconUrl: '/static/images/marker_hole.png',
		number: '',
		shadowUrl: null,
		iconSize: new L.Point(25, 41),
		iconAnchor: new L.Point(13, 41),
		popupAnchor: new L.Point(0, -33),
		/*
		iconAnchor: (Point)
		popupAnchor: (Point)
		*/
		className: 'leaflet-div-icon'
	},

	createIcon: function () {
		var div = document.createElement('div');
		var img = this._createImg(this.options[ 'iconUrl' ]);
		var numdiv = document.createElement('div');
		numdiv.setAttribute("class", "number");
		numdiv.innerHTML = this.options[ 'number' ] || '';
		div.appendChild(img);
		div.appendChild(numdiv);
		this._setIconStyles(div, 'icon');
		return div;
	},

});

const map = L.map('map').setView([ 32, 35 ], 7);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);


$(".suggestions li").each((i, el) => {
	console.log(el);
	const latlng = $(el).data('coords');
	L.marker(latlng, {
		icon: new L.NumberedDivIcon({number: i + 1}),
	}).addTo(map);
	//.bindPopup('A pretty CSS3 popup.<br> Easily customizable.');

});


