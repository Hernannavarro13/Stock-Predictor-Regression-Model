<script lang="ts">
    import { onMount } from 'svelte';
    import type { StockPrediction } from '../lib/api';
    import Chart from 'chart.js/auto';
    import 'chartjs-adapter-date-fns';

    export let prediction: StockPrediction;

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    $: if (prediction && canvas) {
        setupChart();
    }

    function setupChart() {
        if (chart) {
            chart.destroy();
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const currentDate = new Date();
        const predictionDate = new Date(prediction.prediction_date);

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [currentDate, predictionDate],
                datasets: [
                    {
                        label: 'Stock Price',
                        data: [
                            { x: currentDate, y: prediction.current_price },
                            { x: predictionDate, y: prediction.predicted_price }
                        ],
                        borderColor: prediction.predicted_change >= 0 ? '#4CAF50' : '#F44336',
                        backgroundColor: prediction.predicted_change >= 0 ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)',
                        borderWidth: 3,
                        pointBackgroundColor: prediction.predicted_change >= 0 ? '#2E7D32' : '#C62828',
                        pointRadius: 6,
                        pointHoverRadius: 8,
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    title: {
                        display: true,
                        text: `Stock Price Prediction for ${prediction.ticker}`,
                        color: '#E0E0E0',
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    legend: {
                        display: true,
                        labels: {
                            color: '#E0E0E0',
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#FFFFFF',
                        bodyColor: '#FFFFFF',
                        borderColor: '#555555',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: (context) => `Price: $${context.parsed.y.toFixed(2)}`
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            displayFormats: {
                                day: 'MMM d, yyyy'
                            }
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)',
                            borderColor: '#666666'
                        },
                        ticks: {
                            color: '#E0E0E0'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)',
                            borderColor: '#666666'
                        },
                        ticks: {
                            color: '#E0E0E0',
                            callback: (value) => `$${value}`
                        }
                    }
                }
            }
        });
    }

    onMount(() => {
        if (prediction) {
            setupChart();
        }

        return () => {
            if (chart) {
                chart.destroy();
            }
        };
    });
</script>

<div class="chart-container">
    <canvas bind:this={canvas} role="img" aria-label={`Stock price chart for ${prediction?.ticker}`}></canvas>
    <div class="metrics">
        <div class="metric" role="status" aria-live="polite">
            <span class="label">Current Price:</span>
            <span class="value">${prediction.current_price.toFixed(2)}</span>
        </div>
        <div class="metric" role="status" aria-live="polite">
            <span class="label">Predicted Price:</span>
            <span class="value ${prediction.predicted_change >= 0 ? 'positive' : 'negative'}">
                ${prediction.predicted_price.toFixed(2)}
                <span class="change">(${prediction.predicted_change >= 0 ? '+' : ''}${(prediction.predicted_change * 100).toFixed(2)}%)</span>
            </span>
        </div>
    </div>
</div>

<style>
    .chart-container {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 20px;
        height: 400px;
        position: relative;
    }

    .metrics {
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 8px;
        color: white;
        font-family: Arial, sans-serif;
    }

    .metric {
        margin-bottom: 10px;
    }

    .metric:last-child {
        margin-bottom: 0;
    }

    .label {
        font-size: 14px;
        color: #BDBDBD;
        margin-right: 8px;
    }

    .value {
        font-size: 16px;
        font-weight: bold;
    }

    .positive {
        color: #4CAF50;
    }

    .negative {
        color: #F44336;
    }

    .change {
        font-size: 14px;
        margin-left: 5px;
        opacity: 0.8;
    }

    canvas {
        width: 100%;
        height: 100%;
    }
</style> 