<script setup>
import { onMounted, reactive, ref } from 'vue';

// State
const chat = reactive({
  objects: [],
  async get() {
    return await fetch('http://localhost:8000/api/rooms/').then(res => {
      if (!res.ok) throw new Error('Errore durante il caricamento delle stanze');
      return res.json();
    });
  },
  async create(name) {
    return await fetch('http://localhost:8000/api/rooms/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    }).then(async res => {
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Errore durante la creazione');
      return data;
    });
  },
  async update(id, name) {
    return await fetch(`http://localhost:8000/api/rooms/${id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    }).then(async res => {
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Errore durante l\'aggiornamento');
      return data;
    });
  },
  async delete(id) {
    return await fetch(`http://localhost:8000/api/rooms/${id}/`, {
      method: 'DELETE'
    }).then(async res => {
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || 'Errore durante l\'eliminazione');
      }
      return true;
    });
  }
});

// UI State
const newRoomName = ref('');
const editingId = ref(null);
const editingName = ref('');
const isLoading = ref(false);

// Toast Notifications
const notification = reactive({
  message: '',
  type: '', // 'success' | 'error'
  visible: false,
  timer: null
});

const showNotification = (msg, type = 'success') => {
  notification.message = msg;
  notification.type = type;
  notification.visible = true;
  if (notification.timer) clearTimeout(notification.timer);
  notification.timer = setTimeout(() => {
    notification.visible = false;
  }, 4000);
};

// Actions
const loadRooms = async () => {
  isLoading.value = true;
  try {
    const data = await chat.get();
    chat.objects = data.rooms || [];
  } catch (err) {
    showNotification(err.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const handleCreate = async () => {
  const name = newRoomName.value.trim();
  if (!name) {
    showNotification('Il nome della stanza non può essere vuoto', 'error');
    return;
  }
  isLoading.value = true;
  try {
    const newRoom = await chat.create(name);
    chat.objects.unshift(newRoom); // Add to the top
    newRoomName.value = '';
    showNotification('Stanza creata con successo!');
  } catch (err) {
    showNotification(err.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const startEdit = (room) => {
  editingId.value = room.id;
  editingName.value = room.name;
};

const cancelEdit = () => {
  editingId.value = null;
  editingName.value = '';
};

const handleUpdate = async (id) => {
  const name = editingName.value.trim();
  if (!name) {
    showNotification('Il nome non può essere vuoto', 'error');
    return;
  }
  isLoading.value = true;
  try {
    const updatedRoom = await chat.update(id, name);
    const index = chat.objects.findIndex(r => r.id === id);
    if (index !== -1) {
      chat.objects[index] = updatedRoom;
    }
    cancelEdit();
    showNotification('Stanza aggiornata con successo!');
  } catch (err) {
    showNotification(err.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const handleDelete = async (id, name) => {
  if (!confirm(`Sei sicuro di voler eliminare la stanza "${name}"?`)) return;
  isLoading.value = true;
  try {
    await chat.delete(id);
    chat.objects = chat.objects.filter(r => r.id !== id);
    showNotification('Stanza eliminata con successo!');
  } catch (err) {
    showNotification(err.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('it-IT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(() => {
  loadRooms();
});
</script>

<template>
  <section class="py-5">
      <div class="container">
        <!-- Header -->
        <header class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
          <div>
            <h1 class="text-primary">Gestione Stanze</h1>
            <p class="text-white">Aggiungi, modifica ed elimina le stanze della chat in tempo reale</p>
          </div>
        </header>
    
        <!-- Notification Toast -->
        <div v-if="notification.visible" :class="['alert', notification.type === 'success' ? 'alert-success' : 'alert-danger', 'position-fixed top-0 end-0 m-3 shadow-lg']" style="z-index: 1080; min-width: 300px;" role="alert">
          <div class="d-flex align-items-center gap-2">
            <svg v-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
            </svg>
            <div class="fw-medium">{{ notification.message }}</div>
          </div>
        </div>
    
        <!-- Create Room Form -->
        <div class="card shadow-sm border mb-4">
          <div class="card-body text-bg-secondary">
            <h2 class="h5 fw-bold mb-3">Crea Nuova Stanza</h2>
            <form @submit.prevent="handleCreate">
              <div class="input-group">
                <input v-model="newRoomName" 
                        type="text" 
                        placeholder="Es: Stanza Sviluppo, Annunci..."
                        :disabled="isLoading"
                        maxlength="100"
                        class="form-control"/>
                <button type="submit" 
                        :disabled="isLoading || !newRoomName.trim()" 
                        class="btn btn-primary">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span>Crea</span>
                </button>
              </div>
            </form>
          </div>
        </div>
    
        <!-- Rooms Table -->
        <div class="card shadow-sm border-primary">
          <div class="card-header text-bg-primary d-flex justify-content-between align-items-center">
            <h2 class="h5 fw-bold mb-0">Stanze Disponibili</h2>
            <span class="d-none d-sm-inline badge text-bg-light">{{ chat.objects.length }} stanze</span>
          </div>

          <div class="card-body text-bg-dark">
            <div v-if="isLoading && chat.objects.length === 0" class="text-center py-5">
              <div class="spinner-border text-primary mb-3" role="status"></div>
              <p class="text-secondary mb-0">Caricamento stanze in corso...</p>
            </div>
    
            <div v-else-if="chat.objects.length === 0" class="alert alert-info">
              <h3 class="h5 fw-bold">Nessuna stanza disponibile</h3>
              <p class="text-secondary mb-0">Crea la tua prima stanza inserendo un nome qui sopra.</p>
            </div>
    
            <div v-else class="table-responsive">
              <table class="table table-hover align-middle table-dark">
                <caption class="visually-hidden">Lista delle stanze disponibili</caption>
                <thead>
                  <tr>
                    <th class="py-3 text-primary text-uppercase small">ID</th>
                    <th class="py-3 text-primary text-uppercase small">Stanza</th>
                    <th class="py-3 text-primary text-uppercase small">Data Creazione</th>
                    <th class="py-3 text-primary text-uppercase small text-end">Azioni</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="room in chat.objects" :key="room.id" :class="{ 'table-active': editingId === room.id }">
                    <!-- ID -->
                    <td class="text-primary">{{ room.id }}</td>
                    
                    <!-- Name (Display or Input) -->
                    <td>
                      <div v-if="editingId === room.id">
                        <input v-model="editingName" 
                               type="text" 
                               class="form-control form-control-sm" 
                               @keyup.enter="handleUpdate(room.id)"
                               @keyup.esc="cancelEdit"
                               ref="inlineInput" />
                      </div>
                      <div v-else class="d-flex align-items-center gap-2">
                        <span>{{ room.name }}</span>
                      </div>
                    </td>
                    
                    <!-- Date -->
                    <td class="small">{{ formatDate(room.created_at) }}</td>
                    
                    <!-- Actions -->
                    <td class="text-end">
                      <div v-if="editingId === room.id" class="btn-group">
                        <button @click="handleUpdate(room.id)" 
                                :disabled="isLoading" 
                                class="btn btn-sm btn-success">
                          Salva
                        </button>
                        <button @click="cancelEdit" 
                                :disabled="isLoading" 
                                class="btn btn-sm btn-secondary">
                          Annulla
                        </button>
                      </div>
                      <div v-else class="btn-group">
                        <button @click="startEdit(room)" 
                                :disabled="isLoading" 
                                class="btn btn-sm btn-outline-success">
                          Modifica
                        </button>
                        <button @click="handleDelete(room.id, room.name)" 
                                :disabled="isLoading" 
                                class="btn btn-sm btn-outline-danger">
                          Elimina
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
  </section>
</template>
