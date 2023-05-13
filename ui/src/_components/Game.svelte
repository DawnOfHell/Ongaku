<script>
    import PlayersScoreboard from "./PlayersScoreboard.svelte"
    import GameChat from "./GameChat.svelte"
    import SongTimer from "./SongTimer.svelte"
</script>

<div class="grid md:grid-cols-game md:grid-rows-1 grid-cols-2 grid-rows-2 min-h-[80%] m-10">
    <PlayersScoreboard/>
    <SongTimer/>
    <div class="col-span-2 md:col-span-1">
        <GameChat/>
    </div>
</div>
