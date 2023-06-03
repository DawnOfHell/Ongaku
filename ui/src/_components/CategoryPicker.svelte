<script>
    import GenreCard from './GenreCard.svelte'
</script>

<h2>Pick your category:</h2>
<div class="grid grid-cols-4 gap-7 -mx-20 my-10 place-self-stretch">
    <!-- Only used to simulated actual data, will be removed asap -->
    {#each Array(16) as _}
        <GenreCard>Genre</GenreCard>
    {/each}
</div>
