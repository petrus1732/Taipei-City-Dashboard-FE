<!-- Developed by Taipei Urban Intelligence Center 2023 -->

<script setup>
import { ref, computed, defineProps } from "vue";
import { useMapStore } from "../../store/mapStore";
const mapStore = useMapStore();

const props = defineProps([
	"chart_config",
	"activeChart",
	"series",
	"map_config",
]);

const chartOptions1 = ref({
	chart: {
		stacked: true,
		toolbar: {
			show: false,
		},
	},
	colors: props.chart_config.color,
	grid: {
		show: false,
	},
	legend: {
		show: props.chart_config.categories ? true : false,
	},
	markers: {
		size: 3,
		strokeWidth: 0,
	},
	plotOptions: {
		radar: {
			polygons: {
				connectorColors: "#444",
				strokeColors: "#555",
			},
		},
	},
	stroke: {
		show: true,
		width: 2,
	},
	tooltip: {
		custom: function ({ series, seriesIndex, dataPointIndex, w }) {
			// The class "chart-tooltip" could be edited in /assets/styles/chartStyles.css
			return (
				'<div class="chart-tooltip">' +
				"<h6>" +
				w.globals.labels[dataPointIndex] +
				`${
					props.chart_config.categories
						? "-" + w.globals.seriesNames[seriesIndex]
						: ""
				}` +
				"</h6>" +
				"<span>" +
				series[seriesIndex][dataPointIndex] +
				` ${props.chart_config.unit}` +
				"</span>" +
				"</div>"
			);
		},
	},
	xaxis: {
		categories: props.chart_config.categories
			? props.chart_config.categories
			: [],
		labels: {
			offsetY: 5,
			formatter: function (value) {
				return value.length > 7 ? value.slice(0, 6) + "..." : value;
			},
		},
		type: "category",
	},
	yaxis: {
		axisBorder: {
			color: "#000",
		},
		labels: {
			formatter: (value) => {
				return "";
			},
		},
		// To fix a bug when there is more than 1 series
		// Orginal behavior: max will default to the max sum of each series
		max: function (max) {
			if (!props.chart_config.categories) {
				return max;
			}
			let adjustedMax = 0;
			props.series.forEach((element) => {
				const maxOfSeries = Math.max.apply(null, element.data);
				if (maxOfSeries > adjustedMax) {
					adjustedMax = maxOfSeries;
				}
			});
			return adjustedMax * 1.1;
		},
	},
});
const selectedIndex = ref(null);

const parsedSeries = computed(() => {
	const toParse = [...props.series[0].data];
	return toParse.map((item) => item.y);
});
const parsedLabels = computed(() => {
	const toParse = [...props.series[0].data];
	return toParse.map((item) => item.x);
});

const chartOptions = ref({
	chart: {
		type: "polarArea",
		toolbar: {
			show: false,
		},
		height: "500px",
	},
	colors: props.chart_config.color,
	grid: {
		show: false,
	},
	legend: {
		show: false,
		position: "bottom",
	},
	plotOptions: {
		polarArea: {
			rings: {
				strokeWidth: 0.5,
			},
			spokes: {
				strokeWidth: 0,
			},
		},
	},
	dataLabels: {
		enabled: true,
	},
	labels: parsedLabels,
	tooltip: {
		followCursor: false,
		custom: function ({ series, seriesIndex, w }) {
			// The class "chart-tooltip" could be edited in /assets/styles/chartStyles.css
			return (
				'<div class="chart-tooltip">' +
				"<h6>" +
				w.globals.labels[seriesIndex] +
				"</h6>" +
				"<span>" +
				series[seriesIndex] +
				` ${props.chart_config.unit}` +
				"</span>" +
				"</div>"
			);
		},
	},
});

function handleDataSelection(e, chartContext, config) {
	if (!props.chart_config.map_filter) {
		return;
	}
	const toFilter = config.dataPointIndex;
	if (toFilter !== selectedIndex.value) {
		mapStore.addLayerFilter(
			`${props.map_config[0].index}-${props.map_config[0].type}`,
			props.chart_config.map_filter[0],
			props.chart_config.map_filter[1][toFilter]
		);
		selectedIndex.value = toFilter;
	} else {
		mapStore.clearLayerFilter(
			`${props.map_config[0].index}-${props.map_config[0].type}`
		);
		selectedIndex.value = null;
	}
}
// console.log(parsedSeries);
</script>

<template>
	<div v-if="activeChart === 'PolarChart'">
		<apexchart
			width="100%"
			type="polarArea"
			:options="chartOptions"
			:series="parsedSeries"
			@dataPointSelection="handleDataSelection"
		></apexchart>
	</div>
</template>
