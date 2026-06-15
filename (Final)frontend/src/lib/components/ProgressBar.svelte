<script>
  export let current = 1;
  export let total = 20;
  $: percent = Math.round((current / total) * 100);
</script>

<div class="progress-wrap">
  <div class="progress-head">
    <span>{current} / {total}</span>
    <span>{percent}%</span>
  </div>
  <div class="bar">
    <div class="fill" style={`width:${percent}%`}></div>
  </div>
</div>

<style>
  .progress-wrap { margin-bottom: 1rem; }
  .progress-head {
    display: flex;
    justify-content: space-between;
    font-size: 0.95rem;
    margin-bottom: 0.4rem;
  }
  .bar {
    height: 12px;
    border-radius: 999px;
    background: #ede9fe;
    overflow: hidden;
  }
  .fill {
    height: 100%;
    background: linear-gradient(90deg, #a855f7, #ec4899);
  }
</style>
