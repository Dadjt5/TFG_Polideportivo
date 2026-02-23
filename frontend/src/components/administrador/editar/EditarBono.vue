<template>
	<div class="min-vh-100 bg-light">
		<main class="container-fluid mt-2 px-5 py-4">

			<!-- CABECERA -->
			<div class="d-flex justify-content-between align-items-center mb-4">
				<button class="btn btn-secondary rounded-pill" @click="volver">
					← {{ t.return }}
				</button>

				<h1 class="fw-semibold mb-0">
					<p v-if="bono.nombreInstalacion">
						<strong>{{ t.facility }}:</strong> {{ bono.nombreInstalacion }}
					</p>
					<p v-else>
						<strong>{{ t.sport }}:</strong> {{ bono.nombreDeporte }}
					</p>
				</h1>

				<div style="width: 100px"></div>
			</div>

			<div class="row g-4">

				<!-- INFORMACIÓN GENERAL -->
				<div class="col-lg-6">
					<div class="bg-white rounded-3 shadow-sm p-4 h-100">
						<div class="row g-3">

							<!-- USOS -->
							<div class="col-6">
								<span class="fw-medium">{{ t.uses }}:</span>
								<p v-if="!editando">{{ bono.usos }}</p>
								<input v-else type="number" min="1" class="form-control" v-model.number="bono.usos" />
							</div>

							<!-- VALIDEZ -->
							<div class="col-6">
								<span class="fw-medium">{{ t.validity }}:</span>
								<p v-if="!editando">{{ bono.validez }}</p>
								<input v-else type="number" min="1" class="form-control" v-model.number="bono.validez" />
							</div>

						</div>

					</div>
				</div>

				<!-- PRECIOS -->
				<div class="col-lg-6">
					<div class="bg-white rounded-3 shadow-sm p-4 h-100">

						<h4 class="mb-3">
							<i class="bi bi-cash-coin text-success me-2"></i>
							{{ t.prices }}
						</h4>

						<div class="row g-3">

							<div class="col-6">
								<span class="fw-medium">{{ t.priceTDA }}:</span>
								<p v-if="!editando">{{ bono.precioTDA }} €</p>
								<input v-else type="number" step="0.01" min="0" class="form-control" v-model.number="bono.precioTDA" />
							</div>

							<div class="col-6">
								<span class="fw-medium">{{ t.priceUAM }}:</span>
								<p v-if="!editando">{{ bono.precioUAM }} €</p>
								<input v-else type="number" step="0.01" min="0" class="form-control" v-model.number="bono.precioUAM" />
							</div>

							<div class="col-6">
								<span class="fw-medium">{{ t.priceSubscripcion }}:</span>
								<p v-if="!editando">{{ bono.precioAbono }} €</p>
								<input v-else type="number" step="0.01" min="0" class="form-control"
									v-model.number="bono.precioAbono" />
							</div>

							<div class="col-6">
								<span class="fw-medium">{{ t.priceOthers }}:</span>
								<p v-if="!editando">{{ bono.precioOtros }} €</p>
								<input v-else type="number" step="0.01" min="0" class="form-control"
									v-model.number="bono.precioOtros" />
							</div>

						</div>

					</div>
				</div>

				<!-- RELACIONES -->
				<div class="col-12">
					<div class="bg-white rounded-3 shadow-sm p-4">
						<div class="row g-3">

							<!-- INSTALACIÓN -->
							<div class="col-md-6">
								<span class="fw-medium">{{ t.facility }}:</span>
								<p v-if="!editando">
									{{ bono.instalacion_nombre || "—" }}
								</p>

								<select v-else class="form-select" v-model="bono.instalacion">
									<option v-for="i in instalaciones" :key="i.id" :value="i.id">
										{{ i.nombre }}
									</option>
								</select>
							</div>

							<!-- DEPORTE -->
							<div class="col-md-6">
								<span class="fw-medium">{{ t.sport }}:</span>
								<p v-if="!editando">
									{{ bono.deporte_nombre || "—" }}
								</p>

								<select v-else class="form-select" v-model="bono.deporte">
									<option v-for="d in deportes" :key="d.id" :value="d.id">
										{{ d.nombre }}
									</option>
								</select>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- ACCIONES -->
			<div class="d-flex justify-content-center gap-4 mt-5">

				<button v-if="!editando" class="btn btn-primary btn-lg rounded-pill" @click="activarEdicion">
					<i class="bi bi-pencil me-2"></i>
					{{ t.modifyBonuses }}
				</button>

				<template v-else>
					<button class="btn btn-success btn-lg rounded-pill" @click="guardarCambios">
						{{ t.saveChanges }}
					</button>

					<button class="btn btn-secondary btn-lg rounded-pill" @click="cancelarEdicion">
						{{ t.cancel }}
					</button>
				</template>

				<button v-if="!editando" class="btn btn-danger btn-lg rounded-pill" @click="eliminar">
					{{ t.delete }}
				</button>

			</div>

		</main>
	</div>
</template>

<script setup lang="ts">
import { ref, inject, onMounted, type Ref } from 'vue'
import { useRouter } from 'vue-router'

import {
	getBonoDetalle,
	modificarBono,
	eliminarBono,
} from '@/services/abonoBonoService'
import { getInstalacionesSimples, getDeportes } from '@/services/listadoService';

import type { Language } from "@/useI18N";
import { useI18n } from "@/useI18N";

const props = defineProps<{ id: string }>();
const language = inject<Ref<Language>>("language")!;
const t = useI18n(language);
const router = useRouter();

const editando = ref(false);
const bono = ref<any>({});
const bonoOriginal = ref<any>(null);

const instalaciones = ref<any[]>([]);
const deportes = ref<any[]>([]);

function activarEdicion() {
	bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));
	editando.value = true;
}

function cancelarEdicion() {
	bono.value = JSON.parse(JSON.stringify(bonoOriginal.value));
	editando.value = false;
}

function camposModificados() {
	const data: any = {};
	for (const key in bono.value) {
		if (bono.value[key] !== bonoOriginal.value[key]) {
			data[key] = bono.value[key];
		}
	}
	return data;
}

const guardarCambios = async () => {
	const data = camposModificados();
	if (Object.keys(data).length > 0) {
		await modificarBono(bono.value.id, data);
		bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));
		editando.value = false;
	}
};

const eliminar = async () => {
	await eliminarBono(bono.value.id);
	router.back();
};

const volver = () => router.back();

onMounted(async () => {
	const id = parseInt(props.id);
	bono.value = await getBonoDetalle(id);
	bonoOriginal.value = JSON.parse(JSON.stringify(bono.value));

	instalaciones.value = await getInstalacionesSimples();
	deportes.value = await getDeportes();
});
</script>