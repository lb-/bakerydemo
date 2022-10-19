from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    StreamBlock,
    ListBlock,
    StructBlock,
    TextBlock,
)

from wagtail.documents.blocks import DocumentChooserBlock


class BaseStepBlock(StructBlock):
    label = CharBlock()
    description = TextBlock(blank=True, required=False)
    # works - but need it to be something better like user groups?
    lane = ChoiceBlock(
        choices=[
            ("", "Select a lane"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        default="h2",
        blank=True,
        required=False,
    )


    class Meta:
        icon = "placeholder"

class DocumentBlock(BaseStepBlock):

    document = DocumentChooserBlock()

    class Meta:
        icon = "doc-empty"
        label = "Document"

class EndBlock(BaseStepBlock):
    """
    Custom `StructBlock` that represents the end of a process.
    """

    class Meta:
        form_classname="end-block-wrapper"
        icon = "radio-full"
        label = "End"


class EventBlock(BaseStepBlock):
    """
    Custom `StructBlock` that represents an external event.
    """

    class Meta:
        icon = "media"
        label = "Event"


class StartBlock(BaseStepBlock):
    """
    Custom `StructBlock` that represents how a process starts.
    """

    class Meta:
        icon = "radio-empty"
        label ="Start"


class TaskBlock(BaseStepBlock):
    """
    Custom `StructBlock` that represents an activity (task) to perform.
    """

    class Meta:
        icon = "tick"
        label ="Task"


class BaseStepsStreamBlock(StreamBlock):
    task_block = TaskBlock()
    event_block = EventBlock()
    document_block = DocumentBlock()

class GatewayBlock(BaseStepsStreamBlock):

    class Meta:
        icon = "pick"
        label = "Option"


class GatewayListBlock(ListBlock):

    def __init__(self, **kwargs):
        super().__init__(child_block=GatewayBlock(),**kwargs)

class ExclusiveGatewayListBlock(GatewayListBlock):

    class Meta:
        icon = "code"
        label = "Exclusive steps"

class StartStreamBlock(StreamBlock):
    start_block = StartBlock()

    class Meta:
        block_counts = {'start_block': {'min_num': 1, 'max_num': 1}}
        label = "Start"


class StepsStreamBlock(BaseStepsStreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    Should have a list of generic StepBlocks
    A step block can be an activity, end, gateway (OR), event, document
    Also -each thing can have a lane (later)
    """

    # add ability for nested sets of process steps
    exclusive_gateway_block = ExclusiveGatewayListBlock()

    # special end block (should not be able to add steps after end in a Stream)
    end_block = EndBlock()

    class Meta:
        # overall process must have an end step (does not account for nested end steps)
        block_counts = {'end_block': {'min_num': 1}}

