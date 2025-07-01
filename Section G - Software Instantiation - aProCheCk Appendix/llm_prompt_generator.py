def task_bpmn_comparison_generator(filename1: str, content1: str, filename2: str, content2: str):
    task_bpmn_comparison =f"""
    Task description: 
        The following are XML depictions of two versions of BPMN process diagrams of the same process.
        Please compare the content of the two diagrams, categorize the changes according to the change dimension and impact categorization and create a Management Summary of the differences in content.
        Answer in the specified JSON format and guide yourself using the given clarifications and examples. The number of changes should never exceed 20.
        Please always just refer to the names of the elements visible to the user, ids and similar technical identifiers that are not written in a human readable text should be disregarded.
    
    Task Data: \nMost recent version: {filename1}: \n {content1} \n \nOld version of the same document: {filename2}: \n {content2}  \n \n

    Task clarification: 
        Write the textual information of the analysis in a form that is easily understandable for human experts (do not use IDs or other codes, use clear human readable text).
        Please try to combine changes, especially to the control flow of the process, whereever it makes sense based on the content. 
        If for example multiple changes to the control flow only change one logical aspect of the process, they can be combined into one change.
        Example: Two tasks are swapped, leading to the change of 3 seperate control flows - this can be summarized as one major control flow change swapping the position of the elements.
        The response should be structured as a JSON object with the following key-value pairs:

    JSON key-value pairs: 
    1. 'initial_chain_of_thought': Please lay out your chain of thought, on where the contents of the two versions differ and where you identified changes regarding the content of the process in the document.
        Also explain, how you will organize those changes into entries for the technical comparison.

    2. 'technical_comparison': A technical comparison of the two BPMN diagrams of the same process, including change IDs and technical detail. The Change ID should start at c01 and then count up. 

    3. 'content_comparison': A comparison of the content of the two BPMN files, classifying changes to the new version and describing the implications those changes would have on the process. 
        The changes and implications should be described in sufficient detail, to be able to base further analysis on the descriptions. Each change should reference the relevant ID from the technical comparison.

    4. 'change_categorization_chain_of_thought': Please lay out your chain of thought on how you will categorize the different changes that you have identified into major/minor and the bpm change dimensions task/control flow/data/organization.
        Please focus on categorizing the changes into the BPM Change Dimensions task/control flow/data/organization.
 
    5. 'change_categorization': A categorization of the changes to the BPMN file, including: id, categorization and dimension (options: task, control flow, data, organization)
        Categorization clarification: A change should be classified as major, if it could cause incoherence with other documents. Minor changes tend to be negligible and would imply, that no other related textual process documents would need to be changed to adhere to the new version.
        BPM Change Dimensions Clarifications: 
            Task: Changes to the fundamental elements of the workflows, including the introduction of new tasks, the modification of existing tasks or the deletion of obsolete tasks. These changes have a direct impact on the execution and functionality of the process.
                BPMN example of task changes: addition of a new task element, the modification of a task type or the deletion of redundant task elements.
            Control Flow: Changes to the sequence and logic of processes. This includes changes to the order of activities, the logic of control flows, and decision points. Such changes redefine the path and logic by which processes are executed.
                One control flow change has the scope of one logical change to the control flow. If the control flow needs to be adjusted in multiple places to fit a single task into the existing control flow, that is one single control flow change. If two tasks swap places and the control flow needs to be adjusted according to that, that is one control flow change.
                BPMN example of control flow changes: reordering tasks, changing gateway configurations, or adjusting conditional flows.
            Data: Changes in the consumption and production of data within processes. This includes updates to data elements and data handling procedures to ensure that input and output data flows are consistent and aligned with process requirements. 
                BPMN example of data changes: changes to data objects and data associations.
            Organization: Changes to roles, responsibilities and resource allocations within a process. These changes affect who performs certain tasks and how resources are allocated within workflow executions.
                BPMN example of organization changes: reassigning tasks to different roles, updating swim lane assignments, or changing resource distributions

    6. 'management_summary': A brief summary of the main findings from the comparison focusing on the implications of the changes for the process.

    
    General clarifications: 
        a. The ids given in the XML depiction of the process diagrams do not matter, only human readable text matters for the comparison of the content.
        b. Changes that are only visual can be neglected, like the size of pools/swim lanes or the coordinates of elements do not matter, as long as the connections to other elements are still the same and all elements remain in the same pool/swim lane.
        c. Renamings of elements, that only correct the spelling or change the syntax or capitalization of elements can be disregarded. Also the addition/deletion/specification of already implied or irrelevant/trivial information in the name of elements is only a minor change.
        d. Changes to elements or pools that are not part of the process (like the creation of a new empty pool, that is not connected to the process) is only a minor change.
        e. Some changes to process diagrams, like the exchange of a gateway to a conditional connector with the same logic, may not change the process at all and are only syntax.
        f. The IDs of the elements do not matter, if a control flow with a specific id gets for example exchanged for a new control flow connected to the same elements, that is no change at all.


    Respond in the following JSON format:
    {{
         \"initial_chain_of_thought\": \"Explain the main changes found in the two documents and how you will split those up into different changes.\",
         \"technical_comparison\": [
             {{\"id\": \"c01\", \"detail\": \"Technical comparison detail 1\"}},
             {{\"id\": \"c02\", \"detail\": \"Technical comparison detail 2\"}}
         ],
         \"content_comparison\": [
             {{\"id\": \"c01\", \"change\": \"Change description 1\", \"implication\": \"Implication description 1\"}},
             {{\"id\": \"c02\", \"change\": \"Change description 2\", \"implication\": \"Implication description 2\"}}
         ],
         \"change_categorization_chain_of_thought\": \"Explain how you will categorize the changes into major/minor and the bpm change dimensions task/control flow/data/organization\",
         \"change_categorization\": [
             {{\"id\": \"c01\", \"categorization\": \"major/minor\", \"dimension\": \"task/control flow/data/organization\"}},
             {{\"id\": \"c02\", \"categorization\": \"major/minor\", \"dimension\": \"task/control flow/data/organization\"}}
         ],
         \"management_summary\": \"Brief summary of the main findings\",
    }}
    Hint: If there are no changes to be found, the key-value pairs may also stay empty.

    
    Example changes to clarify dimensions and the scope of one change entry:
        Example 1: A new data object (new database) is added and connected to one task. 
            Correct classification: Only one relevant change of type "data", which includes the connection and new element, no other change.

        Example 2: Two tasks swap places and therefore all incoming and outcoming control flows need to be adopted as well.
            Correct Classification: Only one relevant change of type "control flow", as there is only one change to the logic.

        Example 3: The Start and Stop events change swim lane and the size of the pool changes.
            Correct Classification: No major changes, as all changes are just visual or syntax related.

        Example 4: A task is changed to a also have a collapsed sub process, but the sub process is not defined in more detail yet.
            Correct Classification: No major change, as there is no added information or change to the process yet.

        Example 5: A task is renamed from "send email" to "send email entity" and a new empty pool is added called "unrelated business".
            Correct Classification: No maor changes, as the renaming is just syntax, without extra information contentwise and the new pool is not part of the process.

        Example 6: An XOR Gateway is changed to a conditional control flow with the same logic applied to it.
            Correct Classification: No major changes, as there are just syntax/viasual changes.

        Example 7: The internal ID of one entity is changed, while the name and description stays the same and an XOR Gateway is changed to an AND gateway.
            Correct Classification: Only one major control flow change, as only the gateway has changed in a major way. The ID change can be disregarded as it is just background data.

        Example 8: Added two new tasks called 'AB' and 'AC', which will go between task 'A' and task 'B'. The control flow is also adjusted to fit both entiites in.
            Correct classification: Two major task changes and two major control flow changes, as each added task is one change and each change of the control flow to add the respective tasks is also one control flow.
        
        Example 9: A control flow gets deleted and instead, a new control flow is added with a new name/id, but connected to the same elements in the same direction
            Correct Classification: No change at all, as only ids (or names of control flows) have changed, which do not matter

        Example 10: An existing pool that previously was minimized without any elements is expanded, one start element, a connection to Task 'Task 1', one connection to an end element and an end element is added
            Correct Classification: One Organization change, as the pool is expanded, one task change, as the task is added and two control flow changes for the added start and event elements. No other changes should be identified here.
    """

    return task_bpmn_comparison



# ------------------------------------------------------------------------------------------------------------------------------------------------------



def task_txt_coherence_generator(filename1: str, content1: str, txt_filename: str, txt_content: str, stripped_bpmn_comparison_data: str):
    task_txt_coherence = f"""
    Task description:
    The following are the changes identified between two versions of a BPMN model for a business process as well as one related textual document. You will also receive the most recent version of the bpmn model for reference.
    Please check for each identified change from the BPMN models, whether the new version of the models after the change is still coherent with the textual document or whether the document would need to be changed for it to be coherent again. Consider whether the change was previously categorized as major or minor.
    Answer in the specified JSON format and guide yourself using the given clarifications and examples.

    Task Data:
    Structured comparison of the BPMN versions: {stripped_bpmn_comparison_data}
    \n Corresponding related textual document: {txt_filename}: \n{txt_content}
    \n\n Most recent BPMN version only for reference: {filename1}: \n{content1}

    Task Clarification:
    Write the textual information of the analysis in a form that is easily understandable for human experts (do not use IDs or other codes, use clear human readable text).
    The response should be structured as a JSON object with the following key-value pairs:

    JSON key-value pairs:
    1. 'initial_chain_of_thought': Please lay out your chain of thought, on where the changes identifed in the previous comparison conflict with the content of the related textual document.

    2. 'content_comparison': Given the structured comparison of the two BPMN versions and the related textual document, as well as the latest version of the BPMN model for reference, please check for every change identified in the model comparison, whether the new version is incoherent with the textual document.
        Please describe the incoherence that stems from the change and the new changes that would be needed to be made to the content of the textual document to regain coherence across the documents in detail.
        Please dont use any IDs of the elements for the content comparison, but the Names and Descriptions, that are human readable.
     
    3. 'management summary': Provide an extensive management summary for the Process Owner focusing on: 
            a. The changes to the original document, describing them in clear, non technical terms.
            b. The incoherencies identified between the changed original document and the related textual document
            It should be specified in detail how the related document would need to be adapted, in order to be coherent with the changed source document.

    4. 'changes needed': Provide a summary of the changes needed to the related textual document, to restore the coherence with the changed source document.

    5. 'change_categorization_chain_of_thought': Please lay out your chain of thought on how you will categorize the different changes that you have identified into the Change Categorizations (options: Relevant, Unrelated, Negligible) and bpm change dimensions.
        Please focus on categorizing the changes into the Change Categories (Relevant, Unrelated, Negligible), explaining whether the identified changes conflict with the content of the related textual docuemnt, causing incoherence.
        Changes that do not clearly conflict with the existing process described in the related textual document are either unrelated or negligible.

    6. 'classification': A classification of the changes to the BPMN file, according to the changes needed to the related textual document, 
    including: id, categorization (options: Relevant, Unrelated, Negligible) and dimension (options: task, control flow, data, organization)
        Clarifications for Change Categories: 
            Relevant: Every change, that would imply a change needed in the related text document. Major changes in the original document tend to result in relevant changes needed, as long as they are not unrelated.
            Unrelated: Every change, that changes aspects, that are not relevant in the textual document, like adding an additional pool with activities for entites that are not topic of the text document. 
            Negligible: All minor changes that dont affect the semantic content of the process. For example those that are just of visual nature or spelling/syntax changes. Also changes from the diagram, that are still coherent with the textual document are negligible.
        Generally consider, whether the change was classified as major or minor, when choosing the change category.

        BPM Change Dimensions Clarifications: 
            Task: Changes to the fundamental elements of the workflows, including the introduction of new tasks, the modification of existing tasks or the deletion of obsolete tasks. These changes have a direct impact on the execution and functionality of the process.
                BPMN example of task changes: addition of a new task element, the modification of a task type or the deletion of redundant task elements.
            Control Flow: Changes to the sequence and logic of processes. This includes changes to the order of activities, the logic of control flows, and decision points. Such changes redefine the path and logic by which processes are executed.
                One control flow change has the scope of one logical change to the control flow. If the control flow needs to be adjusted in multiple places to fit a single task into the existing control flow, that is one single control flow change. If two tasks swap places and the control flow needs to be adjusted according to that, that is one control flow change.
                BPMN example of control flow changes: reordering tasks, changing gateway configurations, or adjusting conditional flows.
            Data: Changes in the consumption and production of data within processes. This includes updates to data elements and data handling procedures to ensure that input and output data flows are consistent and aligned with process requirements. 
                BPMN example of data changes: changes to data objects and data associations.
            Organization: Changes to roles, responsibilities and resource allocations within a process. These changes affect who performs certain tasks and how resources are allocated within workflow executions.
                BPMN example of organization changes: reassigning tasks to different roles, updating swim lane assignments, or changing resource distributions

    General Clarifications:
    a. The ids given in the XML depiction of the process diagrams do not matter, only human readable text matters for the comparison of the content.
    b. Changes that are only visual can be neglected, like the size of pools/swim lanes or the coordinates of elements do not matter, as long as the connections to other elements are still the same and all elements remain in the same pool/swim lane.
    c. Renaming of elements, that only correct the spelling or change the syntax or capitalization of elements can be disregarded. 
    d. Changes to elements or pools that are not part of the process or elements that do not concern the content of the related textual document is only a unrelated or negligible change.
    e. Renaming elements and only adding/deleting/specifying already implied or irrelevant/trivial information is only a unrelated or negligible change.
    f. If a change does not change anything in addition to the already documented and classified relevant changes, it should be classified as negligible.

    Respond in the following JSON format:
    {{
        \"initial_chain_of_thought\": \"Explain whether the different changes identified in the previous comparison conflict with the related textual document.\",
        \"content_comparison\": [
            {{\"id\": \"c01\", \"detail\": \"content comparison detail 1\"}},
            {{\"id\": \"c02\", \"detail\": \"content comparison detail 2\"}}
        ],
        \"management_summary\": \"Brief summary of the main findings\",
        \"changes_needed\": \"Brief summary of the changes needed to the related textual document, to restore the coherence with the changed source document.\",
        \"change_categorization_chain_of_thought\": \"Explain how you will categorize the changes into the change categories Relevant/Unrelated/Negligible and the bpm change dimensions task/control flow/data/organization\",
        \"classification\": [
            {{\"id\": \"c01\", \"Change Category\": \"Relevant/Unrelated/Negligible\", \"dimension\": \"task/control flow/data/organization\"}},
            {{\"id\": \"c02\", \"Change Category\": \"Relevant/Unrelated/Negligible\", \"dimension\": \"task/control flow/data/organization\"}}
        ],
    }}

    Example changes to clarify dimensions and the change category of a change:
    Example 1: A lane is deleted and the tasks are moved to a different lane with a different role attached, while the textual document still refers to the old role.
        Correct Classification: Changes should be classified as Relevant and organization, as the roles change and the textual documentation has wrong information which is incoherent with the new BPMN model.

    Example 2: Renamed condition from 'if a present' to 'if a is present'
        Correct Classification: Change should be classified as negligible and task or not named at all, as the content of the process is not changed and no incoherence can stem from the change.

    Example 3: Changed a XOR gateway to a conditional connector with the same logic.
        Correct classification: Change should be classified as either negligible and control flow or not named at all, as the content of the process is not changed and no incoherence can stem from the change.

    Example 4: Addition of an empty pool called 'unrelated business' with no connections to any element of the process.
        Correct classification: Change should be classified as either negligible/unrelated and organization or not named at all, as the process itself is not changed.

    Example 5: Name of Database is changed from "MySQL" to "MySQLv2", while the related textual document does not mention any data information at all.
        Correct classification: The change should be classified as unrelated and data, as the change does not change any information present in the textual document, which does not contain any data perspective.

    Example 6: A task is renamed from "decline interview" to "decline interview invitation", while the entire process model and the textual document already solely talk about the interview invitation.
        Correct classification: The change should be classified as task and negligible or not named at all, as the information is already implicit in the rest of the diagram and textual documentation.

    Example 7: Two Tasks swap places in the process and the control flow is changed accordingly.
        Correct classification: The change should be classified as one single relevant control flow change, as there is only one logical change to the control flow.

    Example 8: A new XOR gateway is added to existing control flows including 1 control flow connecting the two gateways, with the gateway logic not being present in the textual document.
        Correct classification: Three relevant control flow changes, one for each new gateway and one for the control flow that has been added.
    """

    return task_txt_coherence




# ------------------------------------------------------------------------------------------------------------------------------------------------------



def management_summary_generator(filename1: str, content1: str, txt_filename: str, txt_content: str, txt_coherence_result: str):
    task_txt_coherence = f"""
    Task description: In a previous step, two versions of a business process document (most likely a bpmn model) have been compared in a structured way 
    and with the results of the comparison, it was checked, whether a related process document (like a process description) is still consistent with the newest changes.
    
    You will now receive the changelog and you task is to create a nicely structured and easily understandable management summary of the changes and the implications for the process and especially the related process document, which will be sent to the process owner.
    Please first describe the changes made to the original document and then describe, how those changes are inconsistent with the related document. 
    Next please describe the implications of the changes that have been made, that are not present in the related document, would have on the described process and what it would mean, if those changes would either be adopted or reverted.
    Lastly, please describe in detail, how the related document would need to be changed, in order to be consistent again with the changed original document.
    
    After writing the management summary, which should fit the main body of an email, please write the title for the email, which the process owner will receive to be notified of the changes.
    This title should be accompanied by an urgengy indicator traffic light indication, which signalizes the urgency and importance of the changes (options: 🟢/🟡/🟠/🔴), with green being the least urgent and important and red being the highest possible urgency and importance to the process and company.

    Task Data:
    Structured comparison of the changes made to the original document and the related text document: {txt_coherence_result}
    \n\n Corresponding related process document only for reference: {txt_filename}: \n{txt_content}
    \n\n Most recent BPMN version only for reference: {filename1}: \n{content1} \n\n

    Respond in the following JSON format:
    {{
        \"management_summary\": \"Comprehensive and structured management summary of the changes and the incoherences with the related process document, which should be used as the text body of an email notification for the process owner\",
        \"Email title\":
            {{\"Urgency and Importancy Rating\": \"🟢/🟡/🟠/🔴\", \"Email Title\": \"Short and comprehensive title for an email notifying the process owner of incoherent changes made to process documentation\"}},
    }}

    Task Clarification:
    a. Only state inconsistencies between the changed new original document and the related process document. Changes to the original process document, that do not imply any needed changes to the related docuemnt need to be omitted.
    b. Write in passive, as the check has been done by the autonomous "aProCheCk" Software.
    c. Write the text in the same languague as the process documents.
    d. The Title should mention the name of the Process and one of the following words incoherence/incoherencies/incoherent
    e. Write the email in correctly formatted Markdown format
    f. Start the email adressing the Process Owner (adressing all genders if german) and end it with greetings from the aProCheCk-Team.
    g. Start the management summary with the changes made to the original document, that are relevant to the related process document, then explain the resulting inconsistencies with the related process document in detail.
        Then describe the implication which would be the result of when the changes are adopted or reverted. and lastly explain the changes needed to the related process docuemnt in detail, in order to reestablish coherence across the process documentation.
    h. The email should mention the name and filetype of both the newest version of the original document as well as the related process document.
    """

    return task_txt_coherence