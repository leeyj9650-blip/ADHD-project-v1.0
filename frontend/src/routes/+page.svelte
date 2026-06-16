<script>
  import { goto } from '$app/navigation';
  import { api } from '$lib/api';
  import { saveUserId } from '$lib/storage';

  let agreed = false;
  let resumeCode = '';
  let resultCode = '';
  let error = '';

  async function resumeSurvey() {
    error = '';
    try {
      const code = resumeCode.trim();
      const data = await api.resumeUser(code);
      saveUserId(data.user.user_id);
      goto('/survey');
    } catch (e) {
      error = e.message;
    }
  }

  async function viewResult() {
    error = '';
    try {
      const code = resultCode.trim();
      await api.getLatestResult(code);
      goto(`/result?user_id=${encodeURIComponent(code)}`);
    } catch (e) {
      error = e.message;
    }
  }
</script>

<div class="page">
  <div class="card">
    <div class="title">ADHD 자가진단 ❤️</div>
    <p class="subtitle">
      본 설문은 ADHD 관련 경향을 스스로 점검해보기 위한 참고용 자가진단입니다.<br />
      결과는 의료적 진단을 대신하지 않으며, 필요 시 전문가 상담을 권장합니다.
    </p>

    <label class="field" style="margin-top:1.5rem;">
      <span class:agreed={agreed}><input type="checkbox" bind:checked={agreed} /> 안내문을 확인했고 동의합니다.</span>
    </label>

    <div class="actions" style="margin-top:1rem;">
      <button class="primary consent-button" class:ready={agreed} disabled={!agreed} on:click={() => goto('/user')}>시작하기</button>
    </div>

    <hr style="margin: 2rem 0; border:none; border-top:1px solid #e5e7eb;" />

    <h3>이어서 하기</h3>
    <div class="grid-2">
      <input bind:value={resumeCode} placeholder="고유번호를 입력하세요" />
      <button class="secondary" on:click={resumeSurvey}>이어서 하기</button>
    </div>

    <h3 style="margin-top:1.5rem;">결과 보기</h3>
    <div class="grid-2">
      <input bind:value={resultCode} placeholder="고유번호를 입력하세요" />
      <button class="secondary" on:click={viewResult}>결과보기</button>
    </div>

    <div class="actions" style="margin-top:1.5rem;">
      <button class="secondary" on:click={() => goto('/admin')}>관리자 결과보기</button>
    </div>

    {#if error}
      <p style="color:#dc2626; margin-top:0.75rem;">{error}</p>
    {/if}
  </div>
</div>
