<template>
    <div class='col col--12'>
        <div class='col col--12 border-b border--gray-light clearfix mb6'>
            <PredictionHeader/>

            <div v-if='prediction.modelLink' class='fr'>
                <button @click='refresh' class='btn fr round btn--stroke btn--gray'>
                    <svg class='icon'><use href='#icon-refresh'/></svg>
                </button>

                <button v-if='complete.includes(stack.status)' @click='deleteStack' class='mr12 btn fr round btn--stroke color-gray color-red-on-hover'>
                    <svg class='icon'><use href='#icon-trash'/></svg>
                </button>
            </div>
        </div>

        <template v-if='meta.environment !== "aws"'>
            <div class='flex-parent flex-parent--center-main pt36'>
                <svg class='flex-child icon w60 h60 color--gray'><use href='#icon-info'/></svg>
            </div>

            <div class='flex-parent flex-parent--center-main pt12 pb36'>
                <h1 class='flex-child txt-h4 cursor-default align-center'>Stacks can only be created when MLEnabler is running in an "aws" environment</h1>
            </div>
        </template>
        <template v-else-if='!prediction || loading.stack || loading.imagery'>
            <div class='flex-parent flex-parent--center-main w-full py24'>
                <div class='flex-child loading py24'></div>
            </div>
        </template>
        <template v-else-if='!prediction.modelLink'>
            <div class='col col--12 py6'>
                <div class='flex-parent flex-parent--center-main pt36'>
                    <svg class='flex-child icon w60 h60 color--gray'><use href='#icon-info'/></svg>
                </div>

                <div class='flex-parent flex-parent--center-main pt12 pb36'>
                    <h1 class='flex-child txt-h4 cursor-default'>A Model must be uploaded before a stack is created</h1>
                </div>
            </div>
        </template>
        <template v-else-if='!imagery || !imagery.length'>
            <div class='flex-parent flex-parent--center-main py12'>
                No imagery sources found to create a stack with
            </div>
        </template>
        <template v-else-if='stack.status === "None"'>
            <h2 class='w-full align-center txt-h4 py12'>Stack Creation</h2>

            <div class='col col--12 grid grid--gut12'>
                <div class='col col--12'>
                    <label>Imagery Source:</label>
                    <div class='border border--gray-light round my12'>
                        <div @click='params.image = img' :key='img.id' v-for='img in imagery' class='col col--12 cursor-pointer bg-darken10-on-hover'>
                            <div class='w-full py6 px6' :class='{
                                "bg-gray-light": params.image.id === img.id
                            }'>
                                <span class='txt-h4 round' v-text='img.name'/>
                                <div v-text='img.fmt' class='fr mx3 bg-blue-faint bg-blue-on-hover color-white-on-hover color-blue px6 py3 round txt-xs txt-bold'></div>
                            </div>
                        </div>
                    </div>
                </div>
                <template v-if='!advanced'>
                    <div class='col col--12'>
                        <button @click='advanced = !advanced' class='btn btn--white color-gray px0'><svg class='icon fl my6'><use xlink:href='#icon-chevron-right'/></svg><span class='fl pl6'>Advanced Options</span></button>
                    </div>
                </template>
                <template v-else>
                    <div class='col col--12 border-b border--gray-light mb12'>
                        <button @click='advanced = !advanced' class='btn btn--white color-gray px0'><svg class='icon fl my6'><use xlink:href='#icon-chevron-down'/></svg><span class='fl pl6'>Advanced Options</span></button>
                    </div>
                </template>
                <template v-if='advanced'>
                    <div class='col col--6 py6'>
                        <label>Max Instance Count</label>
                        <input v-model='params.maxSize' type='text' class='input'>
                    </div>
                    <div class='col col--6 py6'>
                        <label>Max Inference Concurrency</label>
                        <input v-model='params.maxConcurrency' type='text' class='input'/>
                    </div>

                    <div class='col col--12'>
                        <label>Stack Tags</label>
                    </div>

                    <div class='col col--12 grid grid--gut12' :key='tag_idx' v-for='(tag, tag_idx) in params.tags'>
                        <div class='col col--4 py6'>
                            <input v-model='tag.Key' input='text' class='input w-full' placeholder='Key'/>
                        </div>
                        <div class='col col--7 py6'>
                            <input v-model='tag.Value' input='text' class='input w-full' placeholder='Value'/>
                        </div>
                        <div class='col col--1 py6'>
                            <button @click='params.tags.splice(tag_idx, 1)' class='btn btn--stroke round color-gray color-blue-on-hover h36'><svg class='icon'><use href='#icon-close'/></svg></button>
                        </div>
                    </div>

                    <div class='col col--12 py6'>
                        <button @click='params.tags.push({"Key": "", "Value": ""})' class='btn btn--stroke round color-gray color-blue-on-hover'><svg class='icon'><use href='#icon-plus'/></svg></button>
                    </div>
                </template>

                <div class='col col--12 clearfix py12'>
                    <button @click='createStack' class='fr btn btn--stroke color-gray color-green-on-hover round'>Create Stack</button>
                </div>
            </div>
        </template>
        <template v-else-if='submit'>
            <div class='flex-parent flex-parent--center-main w-full'>
                <div class='flex-child py24'>Inferences Submitted</div>
            </div>
            <div class='flex-parent flex-parent--center-main w-full'>
                <button @click='submit = false' class='flex-child btn btn--stroke color-gray color-blue-on-hover round'>Close</button>
            </div>
        </template>
        <template v-else-if='complete.includes(stack.status)'>
            <div class='col col--12 grid'>
                <div class='col col--12 grid'>
                    <span v-text='stack.name'/>
                </div>

                <div class='col col--12 pt12 pb6'>
                    Queue Status

                    <div class='fr'>
                        <button @click='purgeQueue' class='btn mx3 round btn--stroke btn--gray btn--red-on-hover'>
                            <svg class='icon'><use href='#icon-trash'/></svg>
                        </button>
                        <button @click='getQueue' class='btn mx3 round btn--stroke btn--gray'>
                            <svg class='icon'><use href='#icon-refresh'/></svg>
                        </button>
                    </div>
                </div>
                <div class='col col--12 border border--gray-light grid round'>
                    <template v-if='loading.queue'>
                        <div class='flex-parent flex-parent--center-main w-full py24'>
                            <div class='flex-child loading py24'></div>
                        </div>
                    </template>
                    <template v-else>
                        <div class='col col--4'>
                            <div class='align-center'>Queued</div>

                            <div class='align-center' v-text='queue.queued'></div>
                        </div>
                        <div class='col col--4'>
                            <div class='align-center'>Inflight</div>

                            <div class='align-center' v-text='queue.inflight'></div>
                        </div>
                        <div class='col col--4'>
                            <div class='align-center'>Failed</div>

                            <div class='align-center' v-text='queue.dead'></div>

                            <div class='flex-parent flex-parent--center-main col col--12 pb6'>
                                <div class='flex-child'>
                                    <button :disabled='queue.dead === 0' class='btn btn--gray round btn--stroke btn--s'>Resubmit</button>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <div class='col col--12 pt12 flex-parent flex-parent--center-main'>
                    Imagery Chip Submission
                </div>
                <div class='col col--12'>
                    <StackMap
                        v-on:queue='postQueue($event)'
                    />
                </div>
            </div>
        </template>
        <template v-else-if='stack.status !== "None"'>
            <div class='flex-parent flex-parent--center-main w-full py24'>
                <div class='flex-child loading py24'></div>
            </div>
            <div class='flex-parent flex-parent--center-main w-full'>
                <div class='flex-child py24'><span v-text='stack.status'/></div>
            </div>
        </template>
    </div>
</template>

<script>
import PredictionHeader from './PredictionHeader.vue';
import StackMap from './StackMap.vue';

export default {
    name: 'Stack',
    props: ['meta', 'model', 'prediction'],
    data: function() {
        return {
            advanced: false,
            complete: [
                'CREATE_COMPLETE',
                'UPDATE_COMPLETE'
            ],
            loading: {
                stack: true,
                queue: true,
                imagery: true
            },
            queue: {
                queued: 0,
                inflight: 0,
                dead: 0
            },
            looping: false,
            imagery: [],
            params: {
                image: false,
                maxSize: '1',
                maxConcurrency: '50',
                tags: []
            },
            submit: false,
            stack: {
                id: false,
                name: '',
                status: 'None'
            }
        };
    },
    watch: {
        submit: function() {
            this.refresh();
        },
        'params.type': function() {
            if (this.params.type === 'classification') {
                this.params.maxSize = '1';
                this.params.maxConcurrency = '50';
            } else if (this.params.type === 'detection') {
                this.params.maxSize = '5';
                this.params.maxConcurrency = '5';
            }
        }
    },
    mounted: function() {
        this.params.tags = JSON.parse(JSON.stringify(this.model.tags));
        this.refresh();
    },
    methods: {
        refresh: function() {
            if (this.meta.environment === 'aws') {
                this.getStatus();
                this.getQueue();
            }
            this.getImagery();
        },
        purgeQueue: async function() {
            this.loading.queue = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack/tiles`, {
                    method: 'DELETE'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.getQueue();
            } catch (err) {
                this.$emit('err', err);
            }
        },
        getQueue: async function() {
            this.loading.queue = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack/tiles`, {
                    method: 'GET'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(res.message);
                this.queue = body;
                this.loading.queue = false;
            } catch (err) {
                //this.$emit('err', err);
            }
        },
        postQueue: async function(geojson) {
            this.loading.stack = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack/tiles`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(geojson.geometry)
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.submit = true;
                this.loading.stack = false;
            } catch (err) {
                this.$emit('err', err);
            }
        },
        loop: function() {
            this.looping = true;

            if ([
                'None',
                'CREATE_COMPLETE',
                'UPDATE_COMPLETE',
                'DELETE_COMPLETE'
            ].includes(this.stack.status)) {
                this.looping = false;
                return;
            }

            setTimeout(() => {
                if ([
                    'None',
                    'CREATE_COMPLETE',
                    'UPDATE_COMPLETE',
                    'DELETE_COMPLETE'
                ].includes(this.stack.status)) {
                    this.looping = false;
                    return;
                }

                this.loop();
                this.getStatus();
            }, 5000);
        },
        getStatus: async function() {
            this.loading.stack = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack`, {
                    method: 'GET'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.stack = body;
                this.loading.stack = false;

                if (!this.looping) this.loop();
            } catch (err) {
                this.$emit('err', err);
            }
        },
        deleteStack: async function() {
            this.loading.stack = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack`, {
                    method: 'DELETE'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.stack = body;
                this.loading.stack = false;

                if (!this.looping) this.loop();
            } catch (err) {
                this.$emit('err', err);
            }
        },
        getImagery: async function() {
            this.loading.imagery = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/imagery`, {
                    method: 'GET'
                });

                const body = await res.json();

                if (!res.ok) throw new Error(body.message);
                this.imagery = body;

                this.loading.imagery = false;
                if (this.imagery.length === 1) {
                    this.params.image = this.imagery[0];
                }
            } catch (err) {
                this.$emit('err', err);
            }
        },
        emitmode: function(mode) {
            this.$emit('mode', mode);
        },
        createStack: async function() {
            if (!this.params.image) return;
            if (this.params.type === 'classification' && !this.params.inferences) return;

            this.loading.stack = true;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}/prediction/${this.$route.params.predid}/stack`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        tags: this.params.tags.map((tag) => {
                            return {
                                Key: tag.Key,
                                Value: tag.Value
                            };
                        }),
                        imagery: this.params.image.id,
                        maxSize: this.params.maxSize,
                        maxConcurrency: this.params.maxConcurrency
                    })
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.stack = body;
                this.loading.stack = false;

                if (!this.looping) this.loop();
            } catch (err) {
                this.$emit('err', err);
            }
        }
    },
    components: {
        PredictionHeader,
        StackMap
    }
}
</script>
