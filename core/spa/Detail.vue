<template>
    <div class="page">
        <link rel="preload"
              href="/static/vendor/leaflet/images/marker-shadow.png"
              as="image"/>
        <link rel="preload" href="/static/images/marker-icon-green.png"
              as="image">
        <div class="map-container" dir="ltr">

            <l-map :zoom.sync="zoom" :center="center" @click="set_exact_geom"
                   ref="map">
                <l-tile-layer :url="url"
                              :attribution="attribution"></l-tile-layer>
                <l-marker v-if="place" :lat-lng="place.latlng" ref="place">
                    <l-tooltip :content="place.name"/>
                </l-marker>
                <l-marker v-for="(result, index) in search_results"
                          v-bind:key="result.place_id"
                          :lat-lng="result.latlng"
                          :icon="result.icn"
                          @mouseenter="highlight(result, true)"
                          @mouseleave="highlight(result, false)"
                          ref='result'
                >
                    <l-icon
                            :icon="true"
                            :icon-size="[25, 41]"
                            :icon-anchor="[12, 41]"
                            :popup-anchor="[1, -34]"
                            :shadow-size="[41, 41]"
                            icon-url="/static/images/glyph-marker-icon-orange.svg"
                            shadow-url="/static/vendor/leaflet/images/marker-shadow.png"
                    >
                        <div class="icon-text">{{ index + 1 }}</div>
                    </l-icon>

                    <l-tooltip :content="result.display_name"/>

                </l-marker>
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


                <l-marker v-if="exact_geom.latlng"
                          :lat-lng="exact_geom.latlng"
                          ref='exactMarker'>
                    <l-icon
                            :icon="true"
                            icon-url="/static/images/marker-icon-green.png"
                            shadow-url="/static/vendor/leaflet/images/marker-shadow.png"/>

                </l-marker>
                <l-circle v-if="exact_geom.latlng"
                          :lat-lng="exact_geom.latlng"
                          :radius="exact_geom.radius"/>
            </l-map>
        </div>

        <div class="sidebar">

            <div class="photo">
                <img :src="pic_url" :alt="title">
            </div>

            <div class="box">
                <p id="photo-title" @mouseup="copy_search_term()">
                    {{ title }}
                </p>
            </div>


            <div class="columns">
                <div class="column">
                    <div class="is-pulled-left">
                        <form v-on:submit.prevent="">
                            <input type="text" v-model="search_term">
                            <button class="button is-small"
                                    @click="nominatim_search(search_term)">
                                <fa icon="search" size="xs"></fa>
                            </button>
                        </form>
                    </div>
                    <p class="title is-size-5">
                        ישות
                    </p>

                    <a class="panel-block has-background-primary" v-if="place">
                            <span @click="zoom_to(place, 'place')">
                                {{ place.name }}&nbsp;
                            </span>
                        <button class="button is-small"
                                title="Zoom to this place"
                                @click="zoom_to(place, 'place')">
                            <fa icon="search-location"></fa>
                        </button>
                        <button class="button is-small"
                                title="Remove"
                                @click="remove_place()" disabled="1">
                            <fa icon="trash"></fa>
                        </button>
                        <a class="button is-small"
                           :href="osm_url(place.osm_id)" target="_blank"
                           title="Open in OSM">
                            <fa icon="map"></fa>
                        </a>
                    </a>

                    <ol class="suggestions panel" v-if="!saving">

                        <a class="panel-block has-background-warning"
                           v-if="searching">
                            Searching...
                            <fa icon="spinner" spin></fa>
                        </a>

                        <a class="panel-block has-background-warning"
                           v-if="search_results">
                            <div class="is-pulled-right">
                                <button class="button is-small"
                                        @click="search_results=null">
                                    <fa icon="times"></fa>
                                </button>
                            </div>
                            <div class="is-pulled-left">
                                {{search_results.length}} Results.
                            </div>
                        </a>

                        <a class="panel-block has-background-warning"
                           v-for="(result, index) in search_results"
                           :class="{ highlighted: result.highlighted, accepted: result.accepted }"
                           @mouseenter="highlight(result, true)"
                           @mouseleave="highlight(result, false)"
                           :title="result.tip"
                        >
                            <span @click="zoom_to(result, 'result', index)">
                                <b>{{index + 1}}.</b>
                                <img :src="result.icon" vg-if="result.icon">
                                {{ result.display_name }}&nbsp;
                            </span>
                            <button class="button is-small"
                                    title="Zoom to this place"
                                    @click="zoom_to(result, 'result', index)">
                                <fa icon="search-location"></fa>
                            </button>
                            <button class="button is-small"
                                    title="Add"
                                    @click="save_result(result)">
                                <fa icon="save"></fa>
                            </button>
                            <a class="button is-small"
                               :href="nominatim_url(result.place_id)"
                               target="_blank"
                               title="Open in OSM">
                                <fa icon="map"></fa>
                            </a>
                        </a>

                        <a class="panel-block"
                           v-for="(marker, index) in markers"
                           :class="{ highlighted: marker.highlighted, accepted: marker.accepted }"
                           @mouseenter="highlight(marker, true)"
                           @mouseleave="highlight(marker, false)"
                           :title="marker.score"
                        >
                            <span @click="zoom_to(marker, 'marker', index)">
                                <b>{{index + 1}}.</b> {{ marker.name }}&nbsp;
                            </span>
                            <fa v-if="marker.accepted" icon="check"></fa>
                            &nbsp;
                            <button class="button is-small"
                                    title="Zoom to this place"
                                    @click="zoom_to(marker, 'marker', index)">
                                <fa icon="search-location"></fa>
                            </button>
                            <button class="button is-small"
                                    title="Select and save"
                                    @click="save_suggestion(marker, index)">
                                <fa icon="save"></fa>
                            </button>
                        </a>
                    </ol>
                    <div v-else>
                        שומר...
                    </div>
                </div>
                <div class="column">
                    <p class="title">
                        מיקום מדויק
                    </p>

                    <div v-if="!saving_exact">
                        <div v-if="exact_geom.latlng">
                            {{exact_geom.latlng[0]|round(6)}}:{{exact_geom.latlng[1]|round(6)}}
                            <input type="number"
                                   v-model.number="exact_geom.radius"
                                   step="10" min="0">
                            <select v-model.number="exact_geom.radius">
                                <option value="10">10</option>
                                <option value="25">25</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                                <option value="250">250</option>
                                <option value="500">500</option>
                                <option value="1000">1000</option>
                                <option value="2500">2500</option>
                                <option value="5000">5000</option>
                            </select>
                            <button class="button"
                                    @click="remove_exact_geom()">
                                <fa icon="trash" size="xs"></fa>
                            </button>
                        </div>
                        <div v-else>
                            <p>
                                יש ללחוץ על המפה להוספת מיקום מדויק
                            </p>
                        </div>
                        <div v-if="check_exact_geom()">
                            <button @click="save_exact_geom()" class="button">
                                <fa icon="save"></fa>
                            </button>
                        </div>
                    </div>
                    <div v-else>
                        <p>
                            Saving...
                        </p>
                    </div>

                </div>
            </div>

        </div>
    </div>

</template>

<script>
	import {library} from '@fortawesome/fontawesome-svg-core';
	import {
		faCheck,
		faMap,
		faSave,
		faSearch,
		faSearchLocation,
		faSpinner,
		faTimes,
		faTrash,
	} from '@fortawesome/free-solid-svg-icons';
	import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
	import {
		LCircle,
		LIcon,
		LMap,
		LMarker,
		LPopup,
		LTileLayer,
		LTooltip
	} from 'vue2-leaflet';
	import L from 'leaflet';
	import 'leaflet.icon.glyph';

	import axios from 'axios';

	library.add(faSearch);
	library.add(faSearchLocation);
	library.add(faSave);
	library.add(faTrash);
	library.add(faMap);
	library.add(faCheck);
	library.add(faTimes);
	library.add(faSpinner);

	// eslint-disable-next-line
	delete L.Icon.Default.prototype._getIconUrl;
	// eslint-disable-next-line;
	L.Icon.Default.mergeOptions({
		iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
		iconUrl: require('leaflet/dist/images/marker-icon.png'),
		shadowUrl: require('leaflet/dist/images/marker-shadow.png')
	});

	axios.defaults.xsrfHeaderName = "X-CSRFToken";
	axios.defaults.xsrfCookieName = 'csrftoken';
	axios.defaults.headers.common = {
		'X-Requested-With': 'XMLHttpRequest'
	};

	const makeIcon = function (n, opts) {
		const options = {
			prefix: '',
			glyph: n,
			glyphSize: '14px',
			...(opts || {})
		};
		return L.icon.glyph(options);
	};

	export default {
		components: {
			LMap,
			LTileLayer,
			LMarker,
			LTooltip,
			LPopup,
			LIcon,
			LCircle,
			fa: FontAwesomeIcon,
		},
		data() {
			const appData = JSON.parse(document.getElementById('data').innerHTML);

			for (const [ i, m ] of appData.markers.entries()) {
				m.ordinal = i + 1;
				m.icon = makeIcon(m.ordinal);
				m.highlighted = false;
				m.tooltip = '';
			}

			const start = appData.exact_geom.latlng || appData.geom_from_osm;
			return {
				title: appData.title,
				pic_url: appData.pic_url,
				zoom: start ? 11 : 7,
				center: start || [ 32, 35 ],
				url: '//{s}.tile.osm.org/{z}/{x}/{y}.png',
				attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
				markers: appData.markers,
				saving: false,
				saving_exact: false,
				exact_geom: appData.exact_geom,
				original_exact_geom: JSON.stringify(appData.exact_geom),
				exact_geom_changed: false,
				search_term: '',
				search_results: null,
				place: appData.place,
				loaded: false,
				searching: false,
			}
		},
		mounted: function () {
			this.$nextTick(function () {
				console.log(1);
				this.$refs.map.mapObject.invalidateSize();
			})
		}, methods: {
			highlight(marker, v) {
				marker.highlighted = v;
				marker.tooltip = marker.name;
			},
			set_exact_geom(event) {
				if (this.saving_exact) {
					return
				}
				this.exact_geom.latlng = [ event.latlng.lat, event.latlng.lng ];
				if (!this.exact_geom.radius) {
					this.exact_geom.radius = 1000
				}
				this.check_exact_geom();
			},
			remove_exact_geom() {
				this.exact_geom.latlng = null;
				this.exact_geom.radius = null;
				this.check_exact_geom();
			},
			check_exact_geom() {
				this.exact_geom_changed = this.original_exact_geom !== JSON.stringify(this.exact_geom);
				return this.exact_geom_changed;
			},
			zoom_to(marker, ref_name, index = -1) {
				this.center = marker.latlng;
				this.zoom = Math.max(16, this.zoom);
				let ref = this.$refs[ ref_name ];
				if (index > -1) {
					ref = ref[ index ];
				}
				ref.mapObject.openTooltip();
			},
			async save_suggestion(marker, index) {
				this.zoom_to(marker, 'marker', index);
				this.saving = true;
				await axios.post("", {
					'suggestion': marker.id,
				});
				this.saving = false;
				this.markers.forEach(function (m) {
					m.accepted = marker === m;
				});
				this.place = {
					osm_id: marker.osm_id,
					name: marker.name,
					latlng: marker.latlng,
				};

			},
			async save_exact_geom() {
				this.saving_exact = true;
				await axios.post("", {
					'exact_geom': this.exact_geom,
				});
				this.saving_exact = false;
				this.original_exact_geom = JSON.stringify(this.exact_geom);
				this.check_exact_geom();
			},
			copy_search_term() {

				const s = window.getSelection().toString().trim();
				if (s) {
					this.search_term = s;
				}
			},
			async nominatim_search(q) {
				this.searching = true;
				this.search_results = null;
				const url = "https://nominatim.openstreetmap.org/search";
				const resp = await axios.get(url, {
					params: {
						q: q,
						format: 'json',
						limit: 25,
						extratags: 1,
						addressdetails: 1,
						namedetails: 1,
						countrycodes: "il,ps",
						"accept-language": "he",
					}
				});
				this.searching = false;
				this.search_results = resp.data;
				this.search_results.forEach((o, i) => {
					o.latlng = L.latLng(o.lat, o.lon);
					o.ordinal = i + 1;
					o.icn = makeIcon(o.ordinal, {
						iconUrl: "/static/images/glyph-marker-icon-orange.svg",
					});
					o.highlighted = false;
					o.tooltip = '';
					o.tip = `${o.type} ${o.importance.toFixed(2)}`;
				})
			},
			async save_result(result) {
				this.saving = true;
				const osm_id = `${result.osm_type}/${result.osm_id}`;
				const place = {
					osm_id: osm_id,
					name: result.namedetails[ 'name:he' ] || result.namedetails[ 'name' ],
					latlng: [ result.latlng.lat, result.latlng.lng ],
				};
				const resp = await axios.post("", {
					'new_place': place,
				});
				this.saving = false;
				this.place = place;
				this.place.id = resp.data.id;
			},
			osm_url(id) {
				return "https://www.openstreetmap.org/" + id
			},
			nominatim_url(id) {
				return "https://nominatim.openstreetmap.org/details.php?place_id=" + id
			}
		},
		filters: {
			round(value, accuracy) {
				if (typeof value !== 'number') {
					return value;
				}
				return value.toFixed(accuracy).padEnd(9, '0');
			}
		}
	};

</script>

<style>
    @import './node_modules/bulma-rtl/css/bulma-rtl.css';
    @import "./node_modules/leaflet/dist/leaflet.css";

    .page {
        display: flex;
    }

    .map-container {
        flex: 1 1 auto;
        display: flex;
    }

    .sidebar {
        flex: 0 1 auto;
        width: 600px;
        margin: 6px;
        overflow-y: scroll;
    }

    .photo {
        padding: 9px;
        background: #6c6c6c;
        text-align: center;
    }

    .photo img {
        max-width: 100%;
        max-height: 450px;
    }


    .leaflet-div-icon {
        background: transparent;
        border: none;
    }

    .leaflet-marker-icon .number {
        position: relative;
        top: -37px;
        font-size: 12px;
        width: 25px;
        text-align: center;
    }

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
