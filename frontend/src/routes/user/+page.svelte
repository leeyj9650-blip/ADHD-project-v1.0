<script>
  import { goto } from "$app/navigation";
  import { api } from "$lib/api";
  import { saveUserId } from "$lib/storage";

  const regionOptions = [
    "서울",
    "경기",
    "수원",
    "인천",
    "대전",
    "대구",
    "부산",
    "충남",
    "충북",
    "전남",
    "전북",
    "경남",
    "경북",
    "제주",
  ];

  let form = {
    user_name: "",
    gender: "남자",
    age_group: "20대",
    region: "서울",
    consent: true,
  };

  let userCode = "";
  let loading = false;
  let error = "";
  let copied = false;

  async function startSurvey() {
    error = "";
    loading = true;
    copied = false;

    try {
      const data = await api.startUser(form);
      userCode = data.user_id;
      saveUserId(userCode);
      await copyUserCode();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function copyUserCode() {
    if (!userCode) return;

    try {
      await navigator.clipboard.writeText(userCode);
      copied = true;
      setTimeout(() => {
        copied = false;
      }, 1500);
    } catch (e) {
      alert("복사에 실패했습니다. 직접 복사해주세요.");
    }
  }

  function moveSurvey() {
    goto("/survey");
  }
</script>

<div class="page">
  <div class="card">
    <h1>사용자 정보 입력</h1>

    <div class="field">
      <label for="user-name-input">이름 또는 닉네임</label>
      <input
        id="user-name-input"
        bind:value={form.user_name}
        placeholder="예: 홍길동"
      />
    </div>

    <div class="grid-2">
      <div class="field">
        <label for="gender-select">성별</label>
        <select id="gender-select" bind:value={form.gender}>
          <option>남자</option>
          <option>여자</option>
        </select>
      </div>

      <div class="field">
        <label for="age-group-select">연령대</label>
        <select id="age-group-select" bind:value={form.age_group}>
          <option>10대</option>
          <option>20대</option>
          <option>30대</option>
          <option>40대</option>
          <option>50대</option>
          <option>60대</option>
          <option>70대</option>
        </select>
      </div>
    </div>

    <div class="field">
      <label for="region-select">지역</label>
      <select id="region-select" bind:value={form.region}>
        {#each regionOptions as region}
          <option value={region}>{region}</option>
        {/each}
      </select>
    </div>

    <div class="actions">
      <button
        class="primary create-id-button"
        class:ready={form.user_name.trim()}
        disabled={loading || !form.user_name.trim()}
        on:click={startSurvey}
      >
        고유번호 생성
      </button>

      {#if userCode}
        <button class="primary start-survey-button" on:click={moveSurvey}
          >설문 시작</button
        >
      {/if}
    </div>

    {#if error}
      <p style="color:#dc2626;">{error}</p>
    {/if}

    {#if userCode}
      <div class="card" style="margin-top:1.5rem; background:#faf5ff;">
        <h3>고유번호가 생성되었습니다</h3>

        <div
          style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:12px 0;"
        >
          <input
            value={userCode}
            readonly
            style="flex:1; min-width:240px; background:#fff;"
          />
          <button class="secondary" on:click={copyUserCode}>복사</button>
        </div>

        {#if copied}
          <p style="color:#16a34a; font-weight:600;">복사되었습니다.</p>
        {/if}

        <p class="helper">
          이 고유번호는 이어하기 및 결과 다시보기에 사용됩니다.
        </p>
      </div>
    {/if}
  </div>
</div>
