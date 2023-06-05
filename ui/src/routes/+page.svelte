<script>
    import { goto } from '$app/navigation';

    async function handleSubmit(event) {
        const formData = new FormData(event.currentTarget);
        const response = await fetch('/api/players', {
            method: 'POST',
            body: formData,
        });
        if (response.ok) {
            await goto('/play/solo')
        }
    }
</script>

<h1 class="justify-self-center">Welcome to Ongaku Quiz</h1>
<div class="grid">
    <form on:submit|preventDefault={handleSubmit}>
        <input type="text" name="player_name" class="input input-bordered w-full max-w-xs" required />
        <button class="btn btn-primary btn-block" type="submit">Start</button>
    </form>
</div>
