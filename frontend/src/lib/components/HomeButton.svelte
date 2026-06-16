<script>
  import { goto } from '$app/navigation';

  export let confirmLeave = false;
  export let label = '홈으로';
  export let message = '홈으로 이동하시겠습니까?';

  function goHome() {
    if (confirmLeave && !confirm(message)) return;
    goto('/');
  }
</script>

<button type="button" class="home-button" on:click={goHome} aria-label="홈으로 이동">
  <span class="home-icon">🏠</span>
  <span>{label}</span>
</button>
