<script>
  import { BASE_API_URL, api } from '$lib/api';
  import HomeButton from '$lib/components/HomeButton.svelte';

  let login = { admin_id: 'admin', password: '' };
  let authenticated = false;
  let results = [];
  let stats = null;
  let error = '';

  async function signIn() {
    error = '';

    try {
      await api.adminLogin(login);
      authenticated = true;

      const [resultData, statsData] = await Promise.all([
        api.getAdminResults(),
        api.getAdminStats()
      ]);

      results = resultData.data;
      stats = statsData;
    } catch (e) {
      error = e.message;
    }
  }

  function percent(value, total) {
    if (!total) return 0;

    return Math.round((value / total) * 100);
  }
</script>

<div class="page">
  <div class="page-toolbar">
    <HomeButton label="홈으로" />
  </div>

  <div class="card">
    <h1>관리자 화면</h1>

    {#if !authenticated}
      <div class="grid-2">
        <input bind:value={login.admin_id} placeholder="관리자 ID" />
        <input type="password" bind:value={login.password} placeholder="비밀번호" />
      </div>

      <div class="actions" style="margin-top:1rem;">
        <button class="primary" on:click={signIn}>로그인</button>
      </div>

      {#if error}
        <p style="color:#dc2626;">{error}</p>
      {/if}
    {:else}
      <div class="actions" style="margin-bottom:1rem;">
        <a class="secondary" href={`${BASE_API_URL}/admin/download/users`} target="_blank">users.csv 다운로드</a>
        <a class="secondary" href={`${BASE_API_URL}/admin/download/detail`} target="_blank">results.csv 다운로드</a>
      </div>

      {#if stats}
        <div class="card" style="margin-bottom:1rem; background:#faf5ff;">
          <h3>전체 응답 수: {stats.total_responses}</h3>
        </div>

        <div class="grid-2">
          <div class="card">
            <h3>성별 빈도</h3>

            {#each Object.entries(stats.by_gender) as [label, value]}
              <div class="bar-item">
                <!-- [수정됨] 빈 공간 의미가 헷갈리지 않도록 명수와 퍼센트 표시 -->
                <div>{label} ({value}명, {percent(value, stats.total_responses)}%)</div>

                <div class="bar-track">
                  <div class="bar-fill" style={`width:${percent(value, stats.total_responses)}%`}></div>
                </div>
              </div>
            {/each}
          </div>

          <div class="card">
            <h3>연령별 빈도</h3>

            {#each Object.entries(stats.by_age_group) as [label, value]}
              <div class="bar-item">
                <!-- [수정됨] 명수와 퍼센트 표시 -->
                <div>{label} ({value}명, {percent(value, stats.total_responses)}%)</div>

                <div class="bar-track">
                  <div class="bar-fill" style={`width:${percent(value, stats.total_responses)}%`}></div>
                </div>
              </div>
            {/each}
          </div>
        </div>

        <div class="card" style="margin-top:1rem;">
          <h3>지역별 빈도</h3>

          {#each Object.entries(stats.by_region) as [label, value]}
            <div class="bar-item">
              <!-- [수정됨] 명수와 퍼센트 표시 -->
              <div>{label} ({value}명, {percent(value, stats.total_responses)}%)</div>

              <div class="bar-track">
                <div class="bar-fill" style={`width:${percent(value, stats.total_responses)}%`}></div>
              </div>
            </div>
          {/each}
        </div>
      {/if}

      <div class="card" style="margin-top:1rem;">
        <h3>응답 내역 조회</h3>

        <div style="overflow:auto;">
          <table class="table">
            <thead>
              <tr>
                <th>사용자</th>
                <th>User ID</th>
                <th>성별</th>
                <th>연령</th>
                <th>지역</th>
                <th>총점</th>
                <th>부주의</th>
                <th>과잉행동/충동성</th>
              </tr>
            </thead>

            <tbody>
              {#each results as row}
                <tr>
                  <td>{row.User_name}</td>
                  <td>{row.User_id}</td>
                  <td>{row.Gender}</td>
                  <td>{row.Age_group}</td>
                  <td>{row.Region}</td>
                  <td>{row['총점']}</td>
                  <td>{row['부주의 점수']}</td>
                  <td>{row['과잉행동/충동성 점수']}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    {/if}
  </div>
</div>