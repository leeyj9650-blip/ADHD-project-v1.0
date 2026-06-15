<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api';
  import { getUserId } from '$lib/storage';

  let userId = '';
  let items = [];
  let loading = true;
  let error = '';

  onMount(async () => {
    userId = getUserId();
    if (!userId) {
      goto('/');
      return;
    }
    try {
      const data = await api.getReview(userId);
      items = data.items;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  });

  async function updateAnswer(questionId, choiceId) {
    try {
      const numericChoiceId = Number(choiceId);
      await api.updateReviewAnswer({ user_id: userId, question_id: questionId, choice_id: numericChoiceId });
      items = items.map((item) => item.question_id === questionId ? { ...item, selected_choice_id: numericChoiceId } : item);
    } catch (e) {
      error = e.message;
    }
  }

  async function finalize() {
    if (items.some((item) => item.selected_choice_id === null || item.selected_choice_id === undefined)) {
      error = '응답이 없는 문항이 있습니다. 최종 점검에서 모두 선택해주세요.';
      return;
    }
    try {
      const result = await api.finalizeResult(userId);
      sessionStorage.setItem('adhd_result', JSON.stringify(result));
      goto('/result');
    } catch (e) {
      error = e.message;
    }
  }
</script>

<div class="page">
  <div class="card">
    <h1>최종 점검</h1>
    <p class="subtitle">응답한 내용을 확인하고 수정할 수 있습니다.</p>

    {#if loading}
      <p>불러오는 중...</p>
    {:else if error}
      <p style="color:#dc2626;">{error}</p>
    {:else}
      {#each items as item}
        <div class="card" style="margin-bottom:1rem; padding:1rem;">
          <strong>Q{item.question_id}. {item.question}</strong>
          <p class="helper" style="margin-top:0.5rem;">현재 선택: {item.selected_choice_id !== null && item.selected_choice_id !== undefined ? `${item.selected_choice_id + 1}번` : '미응답'}</p>
          <div class="field" style="margin-top:0.75rem;">
            <select bind:value={item.selected_choice_id} on:change={(e) => updateAnswer(item.question_id, e.currentTarget.value)}>
              {#each item.choices as choice}
                <option value={choice.choice_id}>{choice.choice_id + 1}번 - {choice.text}</option>
              {/each}
            </select>
          </div>
        </div>
      {/each}

      <div class="actions">
        <button class="primary" on:click={finalize}>설문 종료 및 결과 보기</button>
      </div>
    {/if}
  </div>
</div>
