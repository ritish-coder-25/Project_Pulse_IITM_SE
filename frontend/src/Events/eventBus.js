// src/eventBus.js
import mitt from 'mitt'

const emitter = mitt()

export const Emitter = emitter
