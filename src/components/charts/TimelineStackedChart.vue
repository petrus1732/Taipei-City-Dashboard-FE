<!-- Developed by Taipei Urban Intelligence Center 2023 -->

<script setup>
import { ref } from "vue";

const props = defineProps(["chart_config", "activeChart", "series"]);

const chartOptions = ref({
	chart: {
		stacked: true,
		toolbar: {
			show: false,
			tools: {
				zoom: false,
			},
		},
	},
	colors: props.chart_config.color,
	dataLabels: {
		enabled: false,
	},
	grid: {
		show: false,
	},
	legend: {
		show: props.series.length > 1 ? true : false,
	},
	markers: {
		hover: {
			size: props.chart_config?.markers?.hover?.size ?? 5,
		},
		size: props.chart_config?.markers?.size ?? 3,
		strokeWidth: props.chart_config?.markers?.strokeWidth ?? 0,
	},
	stroke: {
		colors: props.chart_config.color,
		curve: "smooth",
		show: true,
		width: 2,
	},
	tooltip: {
		custom: function ({ series, seriesIndex, dataPointIndex, w }) {
			// The class "chart-tooltip" could be edited in /assets/styles/chartStyles.css
			return (
				'<div class="chart-tooltip">' +
				"<h6>" +
				`${parseTime(
					w.config.series[seriesIndex].data[dataPointIndex].x
				)}` +
				` - ${w.globals.seriesNames[seriesIndex]}` +
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
		axisBorder: {
			color: "#555",
			height: "0.8",
		},
		axisTicks: {
			show: false,
		},
		crosshairs: {
			show: false,
		},
		tooltip: {
			enabled: false,
		},
		type: "datetime",
	},
});

function parseTime(time) {
	return time.replace("T", " ").replace("+08:00", " ");
}
</script>

<template>
	<div v-if="activeChart === 'TimelineStackedChart'">
		<apexchart
			width="100%"
			height="260px"
			type="area"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>
