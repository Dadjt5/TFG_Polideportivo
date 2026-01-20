<template>
  <div class="min-vh-100 bg-light py-4">
    <main class="container">

      <h2 class="mb-4 text-center fw-bold">{{ t.updateProfile || 'Modificar datos personales' }}</h2>

      <!-- DATOS BÁSICOS -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">Datos básicos</h5>

          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Nombre</label>
              <input type="text" class="form-control" v-model="usuario.nombre" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">Apellidos</label>
              <input type="text" class="form-control" v-model="usuario.apellidos" disabled>
            </div>

            <div class="col-md-4">
              <label class="form-label">DNI</label>
              <input type="text" class="form-control" v-model="usuario.DNI" disabled>
            </div>
          </div>

          <div class="row g-3 mt-3">
            <div class="col-md-4">
              <label class="form-label">Fecha de nacimiento</label>
              <input type="date" class="form-control" v-model="usuario.fechaNacimiento">
            </div>

            <div class="col-md-4">
              <label class="form-label">Teléfono</label>
              <input type="text" class="form-control" v-model="usuario.telefono">
            </div>

            <div class="col-md-4">
              <label class="form-label">Sexo</label>
              <select class="form-select" v-model="usuario.sexo">
                <option value="NINGUNO">Ninguno</option>
                <option value="HOMBRE">Hombre</option>
                <option value="MUJER">Mujer</option>
                <option value="OTRO">Otro</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- DIRECCIÓN -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">Dirección</h5>

          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">Provincia</label>
              <input type="text" class="form-control" v-model="usuario.provincia">
            </div>

            <div class="col-md-4">
              <label class="form-label">Municipio</label>
              <input type="text" class="form-control" v-model="usuario.municipio">
            </div>

            <div class="col-md-4">
              <label class="form-label">Localidad</label>
              <input type="text" class="form-control" v-model="usuario.localidad">
            </div>

            <div class="col-md-4 mt-3">
              <label class="form-label">Código postal</label>
              <input type="text" class="form-control" v-model="usuario.codigoPostal">
            </div>
          </div>
        </div>
      </div>

      <!-- CUENTA BANCARIA -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">Cuenta bancaria</h5>
          <input type="text" class="form-control" v-model="usuario.cuentaBancaria">
        </div>
      </div>

      <!-- DEPORTES FAVORITOS -->
      <div class="card shadow-sm mb-4">
        <div class="card-body">
          <h5 class="fw-semibold mb-3">Deportes favoritos</h5>
          <select class="form-select" v-model="usuario.deportesFavoritos" multiple>
            <option v-for="deporte in deportesDisponibles" :key="deporte.id" :value="deporte.id">
              {{ deporte.nombre }}
            </option>
          </select>
        </div>
      </div>

      <!-- BOTÓN GUARDAR -->
      <div class="text-center mb-5">
        <button class="btn btn-primary btn-lg px-4" @click="guardarCambios">
          Guardar cambios
        </button>
      </div>

    </main>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, defineComponent } from 'vue'
import { useUserStore } from '../stores/usuarioFinal'

const usuarioFinalStore = useUserStore()

const usuario = ref({
  nombre: '',
  apellidos: '',
  DNI: '',
  fechaNacimiento: '',
  telefono: '',
  provincia: '',
  municipio: '',
  localidad: '',
  codigoPostal: '',
  cuentaBancaria: '',
  sexo: 'NINGUNO',
  deportesFavoritos: [] as number[],
})

const deportesDisponibles = ref<{ id: number; nombre: string }[]>([])

onMounted(async () => {
  // Traemos datos del usuario desde el store
  const data = usuarioFinalStore.usuarioFinal
  if (data) {
    usuario.value = {
      ...usuario.value,
      ...data,
      deportesFavoritos: data.deportesFavoritos.map((d: any) => d.id)
    }
  }

  // Traemos deportes disponibles
  //deportesDisponibles.value = await getDeportes()
})

const guardarCambios = async () => {
  try {
    //await actualizarUsuarioFinal(usuario.value)
    alert('Datos actualizados correctamente')
  } catch (error) {
    console.error(error)
    alert('Error al actualizar los datos')
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.75rem 1.25rem rgba(0, 0, 0, 0.15);
}

h2 {
  font-size: 2rem;
}
</style>
