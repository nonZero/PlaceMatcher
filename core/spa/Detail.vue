<template>
    <div class="page">
        <div class="map-container">

            <l-map :zoom.sync="zoom" :center="center">
                <l-tile-layer :url="url"
                              :attribution="attribution"></l-tile-layer>
                <l-marker v-for="(marker, index) in markers"
                          v-bind:key="marker.id"
                          :lat-lng="marker.latlng"
                          :icon="marker.icon"
                          @mouseenter="highlight(marker, true)"
                          @mouseleave="highlight(marker, false)"
                          ref='marker'
                >
                    <l-icon
                            :icon="true"
                            :icon-size="[25, 41]"
                            :icon-anchor="[12, 41]"
                            :popup-anchor="[1, -34]"
                            :shadow-size="[41, 41]"
                            icon-url="/static/vendor/leaflet.icon.glyph/glyph-marker-icon.png"
                            shadow-url="/static/vendor/leaflet/images/marker-shadow.png"
                    >
                        <div class="icon-text">{{ index + 1 }}</div>
                    </l-icon>
                    <l-tooltip :content="marker.name"/>

                </l-marker>

            </l-map>
        </div>

        <div class="sidebar">

            <h1>
                {{ title }}
            </h1>

            <div class="photo">
                <img :src="pic_url">
            </div>

            <ol class="suggestions panel" v-if="!selectedItem">
                <a class="panel-block" v-for="(marker, index) in markers"
                   :class="{ highlighted: marker.highlighted, accepted: marker.accepted }"
                   @mouseenter="highlight(marker, true)"
                   @mouseleave="highlight(marker, false)"
                   :title="marker.score"
                >
                    <span @click="click(marker, index)">
                        {{ marker.name }}
                    </span>
                    <i v-if="marker.accepted" class="fas fa-check"></i>

                    <button class="button is-small"
                            @click="select(marker, index)">
                        Select
                    </button>
                </a>
            </ol>

            <div v-if="selectedItem">
                {{ selectedItem.name }}
                <div v-if="!saving & !saved">
                    <button class="button is-primary" @click="save()">
                        Save
                    </button>
                    <button class="button" @click="selectedItem=null">
                        Cancel
                    </button>
                </div>
                <div v-else>
                    <div v-if="!saved">
                        Saving...
                    </div>
                    <div v-else>
                        Saved!
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
	import axios from 'axios';

	axios.defaults.xsrfHeaderName = "X-CSRFToken";
	axios.defaults.xsrfCookieName = 'csrftoken';
	axios.defaults.headers.common = {
		'X-Requested-With': 'XMLHttpRequest'
	};


	const {LMap, LTileLayer, LMarker, LTooltip, LPopup, LIcon} = Vue2Leaflet;

	const makeIcon = function (n) {
		return L.icon.glyph({
			prefix: '',
			glyph: n,
			glyphSize: '14px',
		});
	};

	window.App = {
		components: {LMap, LTileLayer, LMarker, LTooltip, LPopup, LIcon},
		data() {
			const appData = JSON.parse(document.getElementById('data').innerHTML);

			for (const [ i, m ] of appData.markers.entries()) {
				m.ordinal = i + 1;
				m.icon = makeIcon(m.ordinal);
				m.highlighted = false;
				m.tooltip = '';
			}

			return {
				title: appData.title,
				pic_url: appData.pic_url,
				zoom: 7,
				center: [ 32, 35 ],
				url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
				attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
				markers: appData.markers,
				selectedItem: null,
				saving: false,
				saved: false,
			}
		},
		methods: {
			highlight(marker, v, index) {
				marker.highlighted = v;
				marker.tooltip = marker.name;
			},
			click(marker, index) {
				this.center = marker.latlng;
				this.zoom = Math.max(16, this.zoom);
				const m = this.$refs.marker[ index ].mapObject;
				m.openTooltip();
			},
			select(marker, index) {
				this.click(marker, index);
				this.selectedItem = marker;
			},
			save() {
				this.saving = true;
				axios.post("", {
					'suggestion': this.selectedItem.id,
				}).then(x => {
					console.log(x.data);
					this.saving = false;
					this.saved = true;
				});
			}

		}
	};
	export default window.App;

</script>

<style>

    .suggestions li.highlighted {
        background: yellow;
    }

    .suggestions li.accepted {
        font-weight: bold;
    }

    .suggestions li span {
        font-weight: bold;
        cursor: zoom-in;
    }

    .icon-text {
        margin: 4px 8px;
        font-size: 14px;
        color: white;
        font-weight: bold;
        text-align: center;
    }

</style>
