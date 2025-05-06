export const getPermissions = async () => {
    const permissions = {
        edit: 1,
        view: 0
    }
    if ( !window.BX24 ) {
        console.log("Can't find BX24 libary! See https://dev.1c-bitrix.ru/rest_help/js_library/index.php");
        return permissions.view;
    }
    const [user, users] = await Promise.all([getProfile(), getUsersFromSP()]);
    if ( user !== null && users !== null ) {
        if ( users.includes(user.ID)) {
            return permissions.edit;
        }
    }
    return permissions.view;
};


const getProfile = async () => {
    return await new Promise(
        (resolve) => {
            window.BX24.callMethod(
                "profile",
                {},
                (result) => {
                    const data = result.error() ? null : result.data();
                    resolve(data);
                }
            );
        }
    );
};


const getUsersFromSP = async () => {
    return await new Promise(
        (resolve) => {
            window.BX24.callMethod(
                'crm.item.get',
                {
                    entityTypeId: 1036,
                    id: 1,
                    useOriginalUfNames: 'N',
                },
                (result) => {
                    let data = result.error() ? null : result.data();
                    if ( data !== null ) {
                        const users = data.item?.['ufCrm3_1743591513'] || [];
                        data = users.length > 0 ? users : null;
                    }
                    resolve(data);
                }
            );
        }
    );
};


export const updateBXTask = async (task) => {
    window.BX24.callMethod(
        'tasks.task.update',
        {
            taskId: task.id,
            fields: {
                RESPONSIBLE_ID: task.resourceId,
                START_DATE_PLAN: (new Date(task.time.start)).toISOString(),
                END_DATE_PLAN: (new Date(task.time.end)).toISOString()
            }
        },
        (r) => {
            if (r.error()) {
                console.log(`Task=${task.id}: update error`);
            } else {
                console.log(`Task=${task.id}: successfully updated`);
            };
        }
    );
};
