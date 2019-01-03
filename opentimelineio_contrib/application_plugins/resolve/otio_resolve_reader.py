#
# Copyright 2017 Pixar Animation Studios
#
# Licensed under the Apache License, Version 2.0 (the "Apache License")
# with the following modification; you may not use this file except in
# compliance with the Apache License and the following modification to it:
# Section 6. Trademarks. is deleted and replaced with:
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor
#    and its affiliates, except as required to comply with Section 4(c) of
#    the License and to reproduce the content of the NOTICE file.
#
# You may obtain a copy of the Apache License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Apache License with the above modification is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Apache License for the specific
# language governing permissions and limitations under the Apache License.
#

"""The boilerplate for this reader has been partly taken from work by Pixar and
@avrata to integrate OTIO into RV.
"""

import logging
import os
import opentimelineio as otio

log = logging.getLogger(__name__)


class NoMappingForOtioTypeError(otio.exceptions.OTIOError):
    pass


def get_resolve_session():
    """Runs a set of checks to determine if the Python environment is set up
    correctly and returns the current Davinci Resolve session object.
    """
    if "RESOLVE_SCRIPT_LIB" not in os.environ:
        raise RuntimeError(
            "'RESOLVE_SCRIPT_LIB' not set, please check the Resolve Developer "
            "documentation for the correct configuration."
        )

    if "RESOLVE_SCRIPT_API" not in os.environ:
        raise RuntimeError(
            "'RESOLVE_SCRIPT_API' not set, please check the Resolve Developer "
            "documentation for the correct configuration."
        )

    try:
        import DaVinciResolveScript as dvr_script
    except ImportError:
        raise RuntimeError(
            "Could not import 'DaVinciResolveScript'. Please set your "
            "'PYTHONPATH' to include the Resolve Script module. Check the "
            "Resolve developer documentation for the correct configuration."
        )

    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Cannot get Resolve session object. This can "
                           "either be a setup or a license issue. Davinci "
                           "Resolve free edition does currently not support "
                           "Python script file execution outside of the "
                           "Resolve Console window. Upgrade to Studio to "
                           "enable this feature.")

    return resolve


def read_otio_file(otio_filepath):
    """Read an OTIO complatible file and create a representation in Resolve.

    Args:
        otio_filepath: path to OTIO compatible-file

    Returns:
        Resolve root object (e.g. Timeline)
    """

    resolve = get_resolve_session()

    log.debug("Resolve session object: {}".format(resolve))

    input_otio = otio.adapters.read_from_file(otio_filepath)
    return create_resolve_obj_from_otio(input_otio, resolve)


def create_resolve_obj_from_otio(in_otio, resolve, track_kind=None):
    """Maps and creates a Resolve representation from the OTIO input.

    Args:
        in_otio:
        track_kind:

    Returns:

    """
    otio_type_mapping = {
        otio.schema.Timeline: _create_timeline,
        otio.schema.Stack: _create_stack,
        otio.schema.Track: _create_track,
        otio.schema.Clip: _create_item,
        otio.schema.Gap: _create_item,
        otio.schema.Transition: _create_transition,
    }

    if type(in_otio) in otio_type_mapping:
        return otio_type_mapping[type(in_otio)](in_otio, resolve, track_kind)

    raise NoMappingForOtioTypeError(
         "{} on object: {}".format(type(in_otio), in_otio)
    )


def _create_timeline(in_tl, resolve, track_kind=None):
    return create_resolve_obj_from_otio(in_tl.tracks)


def _create_stack(in_stack, resolve, track_kind=None):
    pass


def _create_track(in_track, resolve, track_kind=None):
    pass


def _create_item(in_item, resolve, track_kind=None):
    pass


def _create_transition(in_transition, resolve, track_kind=None):
    pass


def _create_dissolve(in_dissolve, resolve, track_kind=None):
    pass


def _create_media_reference(in_mediaref, resolve, track_kind=None):
    pass
