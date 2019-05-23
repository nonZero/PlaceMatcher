<template>
    <div>
        <div v-show="data.length">
            <vuetable ref="vuetable"
                      :api-mode="false"
                      :data-manager="dataManager"
                      :fields="fields"
                      :show-sort-icons="true"
            >
                <div slot="actions" slot-scope="props">
                    <button
                            class="ui small button"
                            @click="onActionClicked('edit-item', props.rowData)"
                    >
                        <i class="fa fa-edit"></i>
                    </button>
                </div>

            </vuetable>
        </div>
        <div v-show="!data.length">
            Loading...
        </div>
    </div>
</template>

<script>
	import Vuetable from 'vuetable-2'

	import axios from 'axios';
	import _ from 'lodash';
	//
	// axios.defaults.xsrfHeaderName = "X-CSRFToken";
	// axios.defaults.xsrfCookieName = 'csrftoken';
	axios.defaults.headers.common = {
		'X-Requested-With': 'XMLHttpRequest'
	};
	//

	const fields = [
		{
			name: 'uid',
			title: 'ID',
			sortField: 'uid',
		},
		{
			name: 'status',
			title: 'Status',
			sortField: 'status',
		},
		{
			name: 'title',
			title: 'Title',
			sortField: 'title',
		},
		{
			name: 'place',
			title: 'Place',
			sortField: 'place',
		},
		'actions',
	];
	window.HomeApp = {
		components: {Vuetable},
		data() {
			// const appData = JSON.parse(document.getElementById('data').innerHTML);
			return {
				data: [],
				fields: fields,
			}
		},
		watch: {
			data(newVal, oldVal) {
				this.$refs.vuetable.refresh();
			}
		},
		mounted() {
			axios.get("/all.json").then(response => {
				this.data = response.data.items;
			});
		},

		methods: {
			dataManager(sortOrder, pagination) {
				console.log("DM", this.data.length);
				if (this.data.length < 1) {
					return;
				}

				let local = this.data;

				// sortOrder can be empty, so we have to check for that as well
				if (sortOrder.length > 0) {
					console.log("orderBy:", sortOrder[ 0 ].sortField, sortOrder[ 0 ].direction);
					local = _.orderBy(
						local,
						sortOrder[ 0 ].sortField,
						sortOrder[ 0 ].direction
					);
				}

				return {
					data: local,
				};
			},
			onActionClicked(action, row) {
				console.log("slot actions: on-click", row);
				open(row.edit_url, "_blank");
			}


		}
	};
	export default window.HomeApp;

</script>

<style>

</style>
