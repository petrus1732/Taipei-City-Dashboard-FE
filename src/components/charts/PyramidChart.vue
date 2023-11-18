<!-- Developed by Taipei Urban Intelligence Center 2023 -->

<script setup>
import { ref, computed } from "vue";
import { useMapStore } from "../../store/mapStore";

const props = defineProps([
	"chart_config",
	"activeChart",
	"series",
	"map_config",
]);
const mapStore = useMapStore();

const parsedSeries = computed(() => {
	const e1 = { name: "2歲名額使用比例", data: [] };
	const e2 = { name: "3-5歲名額使用比例", data: [] };
	console.log(props.series[0].data[0]);
	for (let i = 0; i < props.series[0].data.length; i++) {
		e1.data.push(
			props.series[0].data[i] /
				(props.series[0].data[i] + props.series[1].data[i])
		);
		e2.data.push(
			(-1 * props.series[2].data[i]) /
				(props.series[2].data[i] + props.series[3].data[i])
		);
	}
	console.log(e1, e2);
	return [e1, e2];
});

const chartOptions = ref({
	chart: {
		type: "bar",
		height: 220,
		stacked: true,
		toolbar: {
			show: false,
		},
		offsetX: 20,
	},
	colors: props.chart_config.color,
	plotOptions: {
		bar: {
			borderRadius: 4,
			borderRadiusWhenStacked: "all",
			horizontal: true,
			barHeight: "50%",
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		show: false,
	},

	grid: {
		show: false,
	},
	yaxis: {
		min: -1,
		max: 1,
		forceNiceScale: false,
		title: {
			// text: 'Age',
		},
		axisTicks: {
			show: false,
		},
	},
	tooltip: {
		custom: function ({ series, seriesIndex, dataPointIndex, w }) {
			return (
				'<div class="chart-tooltip">' +
				"<h6>" +
				w.globals.labels[dataPointIndex] +
				"</h6>" +
				"<span>" +
				Math.abs(
					Math.round(series[seriesIndex][dataPointIndex] * 10000) /
						100
				) +
				` %` +
				"</span>" +
				"</div>"
			);
		},
		followCursor: true,
	},
	xaxis: {
		categories: props.chart_config.categories,
		labels: {
			// formatter: function (val) {
			// 	return Math.abs(Math.round(10000 * val) / 100) + "%";
			// },
			show: false,
		},
		axisTicks: {
			show: false,
		},
		axisBorder: {
			show: false,
		},
	},
	legend: {
		offsetX: -10,
	},
});

const chartOptions1 = ref({
	chart: {
		offsetY: 15,
		stacked: true,
		toolbar: {
			show: false,
		},
	},
	colors: props.chart_config.color,
	dataLabels: {
		offsetX: 20,
		textAnchor: "start",
	},
	grid: {
		show: false,
	},
	legend: {
		show: false,
	},
	plotOptions: {
		bar: {
			borderRadius: 2,
			distributed: true,
			horizontal: true,
		},
	},
	stroke: {
		colors: ["#282a2c"],
		show: true,
		width: 0,
	},
	// The class "chart-tooltip" could be edited in /assets/styles/chartStyles.css
	tooltip: {
		custom: function ({ series, seriesIndex, dataPointIndex, w }) {
			return (
				'<div class="chart-tooltip">' +
				"<h6>" +
				w.globals.labels[dataPointIndex] +
				"</h6>" +
				"<span>" +
				series[seriesIndex][dataPointIndex] +
				` ${props.chart_config.unit}` +
				"</span>" +
				"</div>"
			);
		},
		followCursor: true,
	},
	xaxis: {
		axisBorder: {
			show: false,
		},
		axisTicks: {
			show: false,
		},
		labels: {
			show: false,
		},
		type: "category",
	},
	yaxis: {
		labels: {
			formatter: function (value) {
				return value.length > 7 ? value.slice(0, 6) + "..." : value;
			},
		},
	},
});

const chartHeight = computed(() => {
	return `${40 + props.series[0].data.length * 24}`;
});

const selectedIndex = ref(null);

function handleDataSelection(e, chartContext, config) {
	if (!props.chart_config.map_filter) {
		return;
	}
	if (config.dataPointIndex !== selectedIndex.value) {
		mapStore.addLayerFilter(
			`${props.map_config[0].index}-${props.map_config[0].type}`,
			props.chart_config.map_filter[0],
			props.chart_config.map_filter[1][config.dataPointIndex]
		);
		selectedIndex.value = config.dataPointIndex;
	} else {
		mapStore.clearLayerFilter(
			`${props.map_config[0].index}-${props.map_config[0].type}`
		);
		selectedIndex.value = null;
	}
}
</script>

<template>
	<div v-if="activeChart === 'PyramidChart'">
		<apexchart
			width="100%"
			:height="chartHeight"
			type="bar"
			:options="chartOptions"
			:series="parsedSeries"
		></apexchart>
	</div>
</template>
