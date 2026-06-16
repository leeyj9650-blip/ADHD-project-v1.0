<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { api } from '$lib/api';
  import { clearUserId, getUserId } from '$lib/storage';

  let result = null;
  let error = '';

  function formatScore(value, max) {
    const score = value ?? 0;
    return `${score}/${max}`;
  }

  onMount(async () => {
    const stored = sessionStorage.getItem('adhd_result');

    if (stored) {
      result = JSON.parse(stored);
      return;
    }

    const queryUserId = $page.url.searchParams.get('user_id');
    const userId = queryUserId || getUserId();

    if (!userId) {
      goto('/');
      return;
    }

    try {
      result = await api.getLatestResult(userId);
    } catch (e) {
      error = e.message;
    }
  });

  function restart() {
    clearUserId();
    sessionStorage.removeItem('adhd_result');
    goto('/');
  }
</script>


<div class="page">

  <div class="card">
    <h1>결과 화면</h1>

    {#if error}

      <p style="color:#dc2626;">
        {error}
      </p>

    {:else if result}

      <div class="result-grid">

        <div class="metric">
          <div class="helper">총점</div>
          <h2>
            {formatScore(
              result.total_score ?? result['총점'],
              100
            )}
          </h2>
        </div>

        <div class="metric">
          <div class="helper">부주의 점수</div>
          <h2>
            {formatScore(
              result.inattention_score ?? result['부주의 점수'],
              50
            )}
          </h2>
        </div>

        <div class="metric">
          <div class="helper">과잉행동/충동성 점수</div>
          <h2>
            {formatScore(
              result.hyperactive_impulsive_score ??
              result['과잉행동/충동성 점수'],
              50
            )}
          </h2>
        </div>

      </div>


      <div
        class="card"
        style="margin-top:1.25rem; background:#faf5ff;"
      >
        <h3>해석 문구</h3>

        <p>
          {result.interpretation ?? result['해석 문구']}
        </p>

        <p class="helper">
          본 결과는 참고용입니다.
          일상생활에서 집중, 충동조절, 과잉행동 등으로
          불편함이 지속된다면
          정신건강의학과 또는 전문 상담기관의 평가를
          받아보시기 바랍니다.
        </p>

      </div>


      <div class="actions" style="margin-top:1rem;">
        <button
          class="primary"
          on:click={restart}
        >
          처음으로
        </button>
      </div>

    {:else}

      <p>결과를 불러오는 중...</p>

    {/if}

  </div>

</div>