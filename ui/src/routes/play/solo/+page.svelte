<script>
    import CategoryPicker from '../../../_components/CategoryPicker.svelte'
    import Game from '../../../_components/Game.svelte'
    import { page } from '$app/stores';

    const roomId = $page.url.searchParams.get('room');
</script>

{#if roomId}
<h1 class="mx-auto">Start guessing!</h1>
<Game/>
{:else}
<h1 class="mx-auto">Play solo</h1>
<div>
    <CategoryPicker/>
</div>
<button class="btn btn-primary mx-auto btn-block">Play</button>
{/if}
