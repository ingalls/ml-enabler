<template>
    <div class="col col--12">
        <div class='col col--12 clearfix py6'>
            <h2 v-if='!newModel' class='fl'>Modify Model</h2>
            <h2 v-else class='fl cursor-default'>Add Model</h2>

            <button @click='$router.push({ path: "/" });' class='btn fr round btn--stroke color-gray color-black-on-hover'>
                <svg class='icon'><use href='#icon-close'/></svg>
            </button>

            <button v-if='!newModel' @click='deleteModel($route.params.modelid)' class='mr12 btn fr round btn--stroke color-gray color-red-on-hover'>
                <svg class='icon'><use href='#icon-trash'/></svg>
            </button>
        </div>
        <div class='border border--gray-light round col col--12 px12 py12 clearfix'>
            <div class='grid grid--gut12'>
                <div class='col col--12 py6'>
                    <label>Model Name</label>
                    <input v-model='model.name' class='input' placeholder='Model Name'/>
                </div>

                <div class='col col--6 py6'>
                    <label>Model Source</label>
                    <input v-model='model.source' class='input' placeholder='Company'/>
                </div>

                <div class='col col--6 py6'>
                    <label>Project Url</label>
                    <input v-model='model.projectUrl' class='input' placeholder='External URL'/>
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
                    <div class='col col--12'>
                        <label>Stack Tags</label>
                    </div>

                    <div class='col col--12 grid grid--gut12' :key='tag_idx' v-for='(tag, tag_idx) in model.tags'>
                        <div class='col col--4 py6'>
                            <input v-model='tag.Key' input='text' class='input w-full' placeholder='Key'/>
                        </div>
                        <div class='col col--7 py6'>
                            <input v-model='tag.Value' input='text' class='input w-full' placeholder='Value'/>
                        </div>
                        <div class='col col--1 py6'>
                            <button @click='model.tags.splice(tag_idx, 1)' class='btn btn--stroke round color-gray color-blue-on-hover h36'><svg class='icon'><use href='#icon-close'/></svg></button>
                        </div>
                    </div>

                    <div class='col col--12 py6'>
                        <button @click='model.tags.push({"Key": "", "Value": ""})' class='btn btn--stroke round color-gray color-blue-on-hover'><svg class='icon'><use href='#icon-plus'/></svg></button>
                    </div>
                </template>

                <div class='col col--12 py12'>
                    <button v-if='!newModel' @click='postModel(true)' class='btn btn--stroke round fl color-gray color-red-on-hover'>Archive Model</button>
                    <button v-if='!newModel' @click='postModel(false)' class='btn btn--stroke round fr color-blue-light color-blue-on-hover'>Update Model</button>
                    <button v-else @click='postModel(false)' class='btn btn--stroke round fr color-green-light color-green-on-hover'>Add Model</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'EditModel',
    props: ['meta'],
    data: function() {
        return {
            newModel: this.$route.name === 'newmodel',
            advanced: false,
            model: {
                name: '',
                source: '',
                projectUrl: '',
                tags: []
            }
        }
    },
    mounted: function() {
        this.getModel();
    },
    methods: {
        postModel: async function(archive) {
            try {
                const res = await fetch(window.api + `/v1/model${!this.newModel ? '/' + this.$route.params.modelid : ''}`, {
                    method: this.$route.params.modelid ? 'PUT' : 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        modelId: !this.newModel ? this.$route.params.modelid : undefined,
                        name: this.model.name,
                        source: this.model.source,
                        projectUrl: this.model.projectUrl,
                        archived: archive ? true : false,
                        tags: this.model.tags
                    })
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.$router.push({ path: '/' });
            } catch (err) {
                this.$emit('err', err);
            }
        },
        getModel: async function() {
            if (this.$route.name === "newmodel") return;

            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}`, {
                    method: 'GET'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message)
                this.model = body;
            } catch (err) {
                this.$emit('err', err);
            }
        },
        deleteModel: async function() {
            try {
                const res = await fetch(window.api + `/v1/model/${this.$route.params.modelid}`, {
                    method: 'DELETE'
                });

                const body = await res.json();
                if (!res.ok) throw new Error(body.message);
                this.$router.push({ path: '/' });
            } catch (err) {
                this.$emit('err', err);
            }
        }
    }
}
</script>
