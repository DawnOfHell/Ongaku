<script>
	import PlayersScoreboard from './PlayersScoreboard.svelte';
	import GameChat from './GameChat.svelte';
	import SongTimer from './SongTimer.svelte';
	import { onMount } from 'svelte';
	let menuOpen = false;
</script>

<div class="flex flex-col md:flex-row grow w-full">
	<div class="md:w-1/3 p-4 md:order-first md:sticky md:top-0">
		<button class="md:hidden" on:click={() => (menuOpen = !menuOpen)}>Toggle Menu</button>
		<div class={`${menuOpen ? 'block' : 'hidden'} md:block`}>
			<PlayersScoreboard />
		</div>
	</div>
	<div class="md:w-1/3 p-4 flex-1">
		<GameChat />
	</div>
	<div class="md:w-1/3 p-4 flex-1">
		<SongTimer />
	</div>
</div>
