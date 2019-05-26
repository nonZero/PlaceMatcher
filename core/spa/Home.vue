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
                        <fa icon="edit"></fa>
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
	import 'bulma-rtl/css/bulma-rtl.css';

	import Vuetable from 'vuetable-2';

	import axios from 'axios';
	import _ from 'lodash';
	import {library} from '@fortawesome/fontawesome-svg-core';
	import {faEdit,} from '@fortawesome/free-solid-svg-icons';
	import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

	axios.defaults.headers.common = {
		'X-Requested-With': 'XMLHttpRequest'
	};

	library.add(faEdit);

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

	export default {
		components: {
			Vuetable,
			fa: FontAwesomeIcon,
		},
		data() {
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
				if (this.data.length < 1) {
					return;
				}

				let local = this.data;

				// sortOrder can be empty, so we have to check for that as well
				if (sortOrder.length > 0) {
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
				open(row.edit_url, "_blank");
			}
		}
	};

</script>

<style>

</style>
