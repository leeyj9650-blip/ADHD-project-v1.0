<script>
  export let choices = [];
  export let selectedChoiceId = null;
  export let onSelect = () => {};
</script>

<div class="choice-grid">
  {#each choices as choice}
    <button
      class:selected={selectedChoiceId === choice.choice_id}
      on:click={() => onSelect(choice.choice_id)}
      type="button"
    >
      <span class="num">{choice.choice_id + 1}</span>
      <span>{choice.text}</span>
    </button>
  {/each}
</div>

<style>
  .choice-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem;
  }

  button {
    border: 1px solid #dbeafe;
    background: #fff;
    border-radius: 20px;
    padding: 1rem;
    font-size: 1rem;
    display: flex;
    gap: 0.8rem;
    align-items: center;
    cursor: pointer;
    min-height: 76px;
    color: #334155;
    box-shadow: 0 8px 18px rgba(30, 64, 175, 0.06);
    transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
  }

  button:hover {
    transform: translateY(-2px);
    border-color: #93c5fd;
  }

  button.selected {
    background: linear-gradient(135deg, #dbeafe, #ede9fe);
    border-color: #6366f1;
    color: #1e3a8a;
    font-weight: 800;
  }

  .num {
    width: 34px;
    height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    background: #eff6ff;
    color: #2563eb;
    font-weight: 900;
    flex: 0 0 auto;
  }

  button.selected .num {
    background: #2563eb;
    color: white;
  }

  @media (max-width: 720px) {
    .choice-grid { grid-template-columns: 1fr; }
  }
</style>
